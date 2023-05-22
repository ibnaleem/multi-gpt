import discord, json, os, asyncio, openai, datetime, random, uuid, string, random
import translators as ts
from googletrans import Translator
from discord.ext import commands
from discord.ui import Button, View, Select, ChannelSelect
from discord import app_commands, Embed, Interaction
from typing import Optional, List
from pytube import YouTube
from langs import langs
from NASA.images import *

chat_log = []

with open('config.json') as f:
    config = json.load(f)

# Access the value of TOKEN
TOKEN = config['TOKEN']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), owner_id=1046920598359638036)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(
        name="/help", url='https://www.twitch.tv/gothamchess'))
    print(f"{bot.user} is online with the ID {bot.user.id}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(e)

# Access the value of TOKEN
KEY = config['API_KEY']

# Setting API Key for OpenAI
openai.api_key = KEY


@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    elif message.content.startswith("!"):
        pass
    else:
        if isinstance(message.channel, discord.DMChannel):
            num = 1
            while num != 0:
                chat_log.append({"role": "user", "content": message.content})

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log
                )

                gpt_response = response["choices"][0]["message"]["content"]

                chat_log.append({"role": "assistant", "content": gpt_response})

                await message.channel.send(response["choices"][0]["message"]["content"])
                num -= 1
                if num == 0:
                    break
