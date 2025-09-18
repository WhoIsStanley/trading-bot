import discord
from dotenv import load_dotenv
from discord.ext import commands
from utils import load_alerts
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
tree = bot.tree

async def load_cog():
    for folder in ["cogs", "tasks"]:
        for filename in os.listdir(f"./{folder}"):
            if filename.endswith(".py"):
                extension_name = f"cogs.{filename[:-3]}"
                try:
                    await bot.reload_extension(extension_name)
                except commands.ExtensionNotLoaded:
                    await bot.load_extension(f"{folder}.{filename[:-3]}")
                    print(f"Loaded {folder}.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    load_alerts()
    await load_cog()
    #sync = await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    #print(f"Synced {len(sync)} commands: {[cmd.name for cmd in sync]}")
    sync = await tree.sync()
    print(f"Synced {len(sync)} commands globally")
    print("Ready!")

bot.run(os.getenv("TOKEN"))

