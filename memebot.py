import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import praw
import random
import os

client = discord.Client()
reddit = praw.Reddit(client_id = os.environ['client_id'], client_secret = os.environ['client_secret'], username = os.environ['username'], password = os.environ['password'], user_agent = 'MemeGrim')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="!help"))
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
                
@client.event
async def on_message(message):
    if message.content.startswith('!'):
        if message.content.find('help') == -1:
            await message.channel.send('List of commands:\n\n!help- To get this menu.\n!meme, !funny, etc- To gets memes and stuff.\n!nsfw- To get not safe for work images.')
        

client.run(os.environ['token'])