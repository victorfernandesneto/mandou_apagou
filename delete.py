import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
channels_list = []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.channel.id in channels_list:
        if message.author == bot.user:
            return
        else:
            await message.delete(delay=60)
    await bot.process_commands(message)


@bot.command()
async def here(ctx):
    channel_id = ctx.channel.id
    if channel_id in channels_list:
        channels_list.remove(channel_id)
        await ctx.send('Aqui me despeço!')
    else:
        await ctx.send('Vou deletar geral, fui!')
        channels_list.append(channel_id)

bot.run(str(os.environ.get('DISCORD_TOKEN')))