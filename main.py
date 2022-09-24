import discord
from discord.ext import commands

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix = '$',
            application_id= 1023134462055301161)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

bot = MyBot()

bot.run("MTAyMzEzNDQ2MjA1NTMwMTE2MQ.GssBos.qMOcjbOkyTPhggmqfuSr93dCTB4_O-YWdhxPo4")