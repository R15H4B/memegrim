import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import praw
import random
import os
import requests

client = discord.Client()
reddit = praw.Reddit(client_id = os.environ['client_id'], client_secret = os.environ['client_secret'], username = os.environ['username'], password = os.environ['password'], user_agent = 'Memebot')

bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="!meme"))
    print("Bot is online!")

# Checks whenever a message is sent by a user
@client.event
async def on_message(message):
    if message.content.startswith('!'):
        if message.content.find(' ') == -1:
            try:
                result = ''
                subreddit = reddit.subreddit(message.content[1:])
                post = subreddit.random()
                if hasattr(post, 'url'):
                    result += '\n' + post.url
                if result != '':
                    await message.channel.send(result)
                else:
                    await message.channel.send('Not supported!')
            except Exception:
                await message.channel.send('No match found!')
                
@bot.command()
async def btc(currency : str):
    """fetches bitcoin price."""
    url = 'https://blockchain.info/ticker'
    resp = requests.get(url)
    btc = resp.json()[currency]
    await bot.say(btc['symbol'] + ' ' + str(btc['last']))

client.run(os.environ['token'])