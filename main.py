import discord
from discord.ext import commands
import json
import requests

#open settings
with open("./config.json") as config_file:
    data=json.load(config_file)

#bot config
token = data["token"]
description = "hi im a bot"
intents=discord.Intents.all()

#bot class
bot = discord.Bot(command_prefix=commands.when_mentioned_or("$"), description=description, intents=intents)

#get quote function
def get_quote():
    response = requests.get('https://stoic-server.herokuapp.com/random')
    json_data = json.loads(response.text)

    quote = json_data[0]['body'] + ' - ' + json_data[0]['author']

    return quote

#exec this when bot is executed
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")

#command ping with name as input
@bot.slash_command()
async def ping(ctx, name):
    await ctx.respond(f"Pong! Our bots ping is {bot.latency} seconds, your name is {name}")

#quote command
@bot.slash_command()
async def quote(ctx):
    quote = get_quote()
    await ctx.respond(quote)


#start the bot with the token
bot.run(token)