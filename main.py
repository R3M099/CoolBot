import discord
from discord.ext import commands
from bot import Coolbot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

if __name__ == "__main__":
    bot = Coolbot()

    for name in os.listdir("./cogs"):
        if name.endswith(".py"):
            bot.load_extension("cogs.{}".format(name[:-3]))
    
    bot.run(token)