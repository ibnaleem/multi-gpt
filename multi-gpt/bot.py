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
