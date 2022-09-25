import discord
from discord.ext import commands
import json
import requests
import asyncio
import pymongo
import time
import datetime

#mongodb config
client = pymongo.MongoClient("mongodb+srv://silva:Thisisapassword123@cluster0.fdnupvv.mongodb.net/?retryWrites=true&w=majority")
db = client.journalEntries

print(db)

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

#quote command
@bot.slash_command(description="Get shown a random Stoic quote!")
async def quote(ctx):
    quote = get_quote()
    await ctx.respond(quote)

#journal command
@bot.slash_command(description="Add an entry to your journal")
async def journal(ctx, message):
    today = str(time.strftime("%d-%m-%Y")) 
    #HOW TO INSERT INTO MONGODB
    db.journalMessages.insert_one(
        {
            "message": message,
            "author": ctx.author.id,
            "date": today,
        }
    )
    #notify the user that their message was uploaded to the db
    await ctx.respond('Your message has been journaled.', ephemeral=True)


#myjournal command
@bot.slash_command(description="Shows all your journal entries")
async def myjournal(ctx):
    #get users id
    author = ctx.author.id
    #this makes the db look for any key entry in author which the author id, basically a select * where author=authorid
    key = {'author': author}


    #because there might be more than 1 entry, for loop to print all messages
    responseMessages = []
    responseMessagesDate = []
    str = ""
    strDate = ""
    for m in db.journalMessages.find(key):
        responseMessages.append(m['message'])

    for d in db.journalMessages.find(key):
        responseMessagesDate.append(m['date'])
    
    for msg in responseMessages:
        str += msg + '\n\n'

    for msgDate in responseMessagesDate:
        strDate += msgDate
        
    #print (m['message']) debugging
    if str != "":
        text1 = 'Your journal entries are:\n\n' + str
        await ctx.respond(text1, ephemeral=True)
    else:
        text2 = 'Your journal is empty!'
        await ctx.respond(text2, ephemeral=True)


#myjournaldate command
@bot.slash_command(description="Date in dd-mm-YYYY, filter journal by date")
async def myjournaldate(ctx, date):
    format = "%d-%m-%Y"
    try:
        datetime.datetime.strptime(date, format)
        #get users id
        author = ctx.author.id
        #this makes the db look for any key entry in author which the author id, basically a select * where author=authorid
        key = {
            'author': author,
            'date': date, }

        #because there might be more than 1 entry, for loop to print all messages
        responseMessagesDate = []
        str = ""
        for m in db.journalMessages.find(key):
            responseMessagesDate.append(m['message'])
    
        for msgDate in responseMessagesDate:
            str += msgDate + '\n\n'\
            
        #print (m['message']) debugging
        if str != "":
            await ctx.respond('Your journal entries  for ' + date + ' are:\n\n' + str, ephemeral=True)
        else:
            await ctx.respond('You haven\'t journaled this day!', ephemeral=True)
    except:
        await ctx.respond('The correct date syntax is dd-mm-YYYY!', ephemeral=True)
    



#start the bot with the token
bot.run(token)