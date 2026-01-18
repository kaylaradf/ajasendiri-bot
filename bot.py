import discord
import re
import os
from discord.ext import commands
from dotenv import load_dotenv
from config import WORDLIST_CONFIG, CHAR_REPLACEMENTS

# Load environment variables from .env file
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set")
        exit(1)
    bot.run(TOKEN)