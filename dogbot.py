import asyncio
import json

import discord
from discord.ext import commands
from redis import Redis
from rq import Queue

from golem import generate_image

q = Queue(connection=Redis())


intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True

env = json.load(open("env.json","r"))

PREFIX = '/'

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
TOKEN = env["token"]


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.content.startswith(PREFIX):
        command, *args = message.content.split(" ")
        if command == "/generate":
            job = q.enqueue(generate_image, " ".join(args), job_timeout='1h')
            await message.reply(f"adding request: \"{' '.join(args)}\" to the queue")
            while not job.get_status(refresh=True) == 'finished':
                await asyncio.sleep(1)
            await message.reply(' '.join(args), file=discord.File(job.result))
    
bot.run(TOKEN)
