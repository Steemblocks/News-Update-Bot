import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Load configuration
def load_config():
    """Load configuration from config.json or environment variables"""
    config = {}
    
    # Try to load config.json
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
            print("[OK] Loaded configuration from config.json")
        else:
            print("[WARN] config.json not found, using environment variables")
    except Exception as e:
        print(f"[WARN] Error loading config.json: {e}, using environment variables")
    
    return config

config = load_config()

# Get bot token from config.json or environment
bot_token = config.get("bot", {}).get("token") or os.getenv("DISCORD_TOKEN")
bot_prefix = config.get("bot", {}).get("prefix", "!") or os.getenv("BOT_PREFIX", "!")

if not bot_token:
    raise ValueError("[ERROR] DISCORD_TOKEN not found in config.json or environment variables!")

# Configure logging
log_level = config.get("logging", {}).get("level", "INFO")
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger(__name__)

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=bot_prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Error syncing commands: {e}")

async def load_cogs():
    """Load all cogs from the cogs directory"""
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"bot.cogs.{filename[:-3]}")
            logger.info(f"Loaded cog: {filename}")

async def main():
    """Main function to start the bot"""
    async with bot:
        try:
            await load_cogs()
            logger.info(f"Starting Discord News Bot with token: {bot_token[:20]}...")
            await bot.start(bot_token)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
