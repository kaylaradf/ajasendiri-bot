import discord
import re
import os
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from config import WORDLIST_CONFIG, CHAR_REPLACEMENTS, VOICE_CONFIG

# Load environment variables from .env file
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Voice state
voice_client = None
is_playing = False

def detect_wordlist(text):
    """Detect which wordlist matches the text and return config key"""
    text_lower = text.lower()
    
    # Apply character replacements
    for symbol, letter in CHAR_REPLACEMENTS.items():
        text_lower = text_lower.replace(symbol, letter)
    
    for config_key, config in WORDLIST_CONFIG.items():
        # Only fuzzy matching
        words = re.findall(r'[a-z]+', text_lower)
        keywords_found = {keyword: False for keyword in config['keywords']}
        
        for word in words:
            for keyword in config['keywords']:
                if word in config['fuzzy_words'][keyword]:
                    keywords_found[keyword] = True
        
        if all(keywords_found.values()):
            return config_key
    
    return None

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    detected_wordlist = detect_wordlist(message.content)
    if detected_wordlist:
        config = WORDLIST_CONFIG[detected_wordlist]
        try:
            with open(config['image'], 'rb') as f:
                file = discord.File(f, os.path.basename(config['image']))
                await message.reply(file=file)
        except FileNotFoundError:
            await message.reply(f"Gambar {config['image']} tidak ditemukan!")
    
    await bot.process_commands(message)

def play_audio(voice_client):
    """Play audio with high quality settings"""
    global is_playing
    if not os.path.exists(VOICE_CONFIG['audio_file']):
        print(f"Audio file {VOICE_CONFIG['audio_file']} not found!")
        return
    
    is_playing = True
    audio_source = discord.FFmpegPCMAudio(
        VOICE_CONFIG['audio_file'],
        options=f"-stream_loop -1 -b:a {VOICE_CONFIG['bitrate']}k"
    )
    # Apply volume transformation for background opacity
    audio_source = discord.PCMVolumeTransformer(audio_source, volume=VOICE_CONFIG['volume'])
    voice_client.play(audio_source, after=lambda e: print(f'Error: {e}') if e else None)

@bot.tree.command(name="join", description="Join voice channel and play audio loop")
async def join(interaction: discord.Interaction):
    global voice_client, is_playing
    
    if not interaction.user.voice:
        await interaction.response.send_message("Kamu harus ada di voice channel!", ephemeral=True)
        return
    
    channel = interaction.user.voice.channel
    
    if voice_client and voice_client.is_connected():
        await interaction.response.send_message("Bot sudah di voice channel!", ephemeral=True)
        return
    
    try:
        voice_client = await channel.connect()
        play_audio(voice_client)
        await interaction.response.send_message(f"Joined {channel.name} dan mulai play audio loop!")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

@bot.tree.command(name="stop", description="Stop audio but stay in voice channel")
async def stop(interaction: discord.Interaction):
    global voice_client, is_playing
    
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("Bot tidak ada di voice channel!", ephemeral=True)
        return
    
    if voice_client.is_playing():
        voice_client.stop()
        is_playing = False
        await interaction.response.send_message("Audio stopped, bot masih di channel.")
    else:
        await interaction.response.send_message("Tidak ada audio yang diplay!", ephemeral=True)

@bot.tree.command(name="play", description="Resume playing audio loop")
async def play(interaction: discord.Interaction):
    global voice_client, is_playing
    
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("Bot tidak ada di voice channel!", ephemeral=True)
        return
    
    if voice_client.is_playing():
        await interaction.response.send_message("Audio sudah diplay!", ephemeral=True)
        return
    
    play_audio(voice_client)
    await interaction.response.send_message("Audio resumed!")

@bot.tree.command(name="volume", description="Set audio volume (0.0 - 1.0)")
@app_commands.describe(level="Volume level (0.0 = mute, 1.0 = max, 0.15 = background)")
async def volume(interaction: discord.Interaction, level: float):
    global voice_client
    
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("Bot tidak ada di voice channel!", ephemeral=True)
        return
    
    if level < 0.0 or level > 1.0:
        await interaction.response.send_message("Volume harus antara 0.0 - 1.0!", ephemeral=True)
        return
    
    if voice_client.source:
        voice_client.source.volume = level
        await interaction.response.send_message(f"Volume diset ke {level:.2f} ({int(level*100)}%)")
    else:
        await interaction.response.send_message("Tidak ada audio yang diplay!", ephemeral=True)

@bot.tree.command(name="leave", description="Leave voice channel")
async def leave(interaction: discord.Interaction):
    global voice_client, is_playing
    
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("Bot tidak ada di voice channel!", ephemeral=True)
        return
    
    await voice_client.disconnect()
    voice_client = None
    is_playing = False
    await interaction.response.send_message("Left voice channel.")

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set")
        exit(1)
    bot.run(TOKEN)