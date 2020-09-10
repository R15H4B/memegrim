import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import praw
import random
import os

client = discord.Client()
reddit = praw.Reddit(client_id = os.environ['client_id'], client_secret = os.environ['client_secret'], username = os.environ['username'], password = os.environ['password'], user_agent = 'Memebot')

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
                
@client.event
async def on_message(message):
    if message.content.startswith('$'):
        if message.content.find(' ') == -1:
            try:
			cid = getCID(update)
			url = "https://api.coindesk.com/v1/bpi/currentprice.json"
			data = getJson(url)
			USD = data['bpi']['USD']['rate']
			time = data['time']['updated']
			output = "`1 BTC = $" + USD + "\n\n" + time + "`"
			bot.send_message(cid, output, parse_mode="Markdown")
		except:
			bot.send_message(cid, "`Something went wrong, please wait a moment and try again.`", parse_mode="Markdown")

info = {	'triggers'	:	('btc', 'bitcoin'),
			'name'		:	'bitcoin',
			'help'		: 	"Returns the updated BTC rate from CoinDesk.",
			'example'	:	'',
			'active'	: 	True,
			'admin'		: 	False,
			'arguments' :	""}

client.run(os.environ['token'])
