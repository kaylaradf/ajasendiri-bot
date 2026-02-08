import discord
import re
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from config import WORDLIST_CONFIG, CHAR_REPLACEMENTS

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

@bot.tree.command(name="join", description="Join voice channel and stay (deafened)")
async def join(interaction: discord.Interaction):
    global voice_client
    
    if not interaction.user.voice:
        await interaction.response.send_message("Kamu harus ada di voice channel!", ephemeral=True)
        return
    
    channel = interaction.user.voice.channel
    
    if voice_client and voice_client.is_connected():
        await interaction.response.send_message("Bot sudah di voice channel!", ephemeral=True)
        return
    
    # Defer response to prevent timeout
    await interaction.response.defer()
    
    try:
        voice_client = await channel.connect(self_deaf=True)
        await interaction.followup.send(f"Joined {channel.name} dan stay (deafened)!")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)

@bot.tree.command(name="leave", description="Leave voice channel")
async def leave(interaction: discord.Interaction):
    global voice_client
    
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("Bot tidak ada di voice channel!", ephemeral=True)
        return
    
    await voice_client.disconnect()
    voice_client = None
    await interaction.response.send_message("Left voice channel.")

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set")
        exit(1)
    bot.run(TOKEN)