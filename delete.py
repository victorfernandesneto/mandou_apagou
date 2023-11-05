import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.channel.id == int((os.environ.get('DISCORD_CHANNEL'))):
        await message.delete(delay=60)

print(str(os.environ.get('DISCORD_TOKEN')))
bot.run(str(os.environ.get('DISCORD_TOKEN')))