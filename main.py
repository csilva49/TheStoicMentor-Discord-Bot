import discord
from discord.ext import commands
import json

with open("./config.json") as config_file:
    data=json.load(config_file)

token = data["token"]

description = "hi im a bot"

intents=discord.Intents.all()

bot = discord.Bot(command_prefix=commands.when_mentioned_or("$"), description=description, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")

#command ping with name as input
@bot.slash_command()
async def ping(ctx, name):
    await ctx.respond(f"Pong! Our bots ping is {bot.latency} seconds, your name is {name}")



bot.run(token)