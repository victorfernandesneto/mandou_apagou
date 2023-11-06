import discord
from discord.ext import commands, tasks
import typing
import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute('SELECT * FROM channels')
data = cur.fetchall()

channels_dict = {}
for item in data:
    channels_dict[item[0]] = item[1]

cur.close()
conn.close()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def checa_canal(channel_id):
    if channel_id in channels_dict:
        return True
    return False


@bot.event
async def on_ready():
    clear_loop.start()
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    channel_id = str(message.channel.id)
    if channel_id in channels_dict:
        if message.author == bot.user:
            return
        else:
            delete_time = channels_dict[channel_id]
            await message.delete(delay=delete_time)
    await bot.process_commands(message)


@bot.command()
async def eraseevidence(ctx, time: typing.Optional[int] = 60):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    channel_id = str(ctx.channel.id)
    await ctx.message.delete()
    if checa_canal(channel_id):
        cur.execute('DELETE FROM channels WHERE channel_id = %s', (channel_id,))
        del channels_dict[channel_id]
        await ctx.send("I'm out!", delete_after=5.0)
    else:
        cur.execute('INSERT INTO channels (channel_id, time) VALUES (%s, %s)', (channel_id, time,))
        channels_dict[channel_id] = time
        await ctx.send("You haven't seen nothing!", delete_after=5.0)
    conn.commit()
    cur.close()
    conn.close()


@bot.command()
async def check(ctx):
    channel_id = str(ctx.channel.id)
    await ctx.message.delete()
    if checa_canal(channel_id):
        await ctx.send("Still here!", delete_after=5.0)
    else:
        await ctx.send("Nope, didn't ask me to!", delete_after=5.0)


@tasks.loop(minutes=5)
async def clear_loop():
    for channel_id in channels_dict.keys():
        if checa_canal(channel_id):
            await clear(channel_id)


async def clear(channel_id):
    channel = bot.get_channel(int(channel_id))
    await channel.purge()


if __name__ == '__main__':
    bot.run(str(os.environ.get('DISCORD_TOKEN')))
