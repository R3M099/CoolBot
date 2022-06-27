import discord
from discord.ext import commands
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("PASSWORD")

DEFAULT_PREFIX = "-"

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    
    prefix = await bot.db.fetch("SELECT prefix FROM guilds WHERE guildid = $1", message.guild.id)

    if len(prefix) == 0:
        await bot.db.execute("INSERT INTO guilds (guildid, prefix) VALUES ($1, $2)", message.guild.id, DEFAULT_PREFIX)
        prefix = DEFAULT_PREFIX
    else:
        prefix = prefix[0].get("prefix")
    
    return commands.when_mentioned_or(prefix)(bot, message)

class Coolbot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix = get_prefix,
                         help_command = None,
                         case_insensitive = True,
                         description = "This is a cool bot",
                         intents = discord.Intents.all(),
                         allowed_mentions = discord.AllowedMentions(everyone = False, roles = False),
                         **options)
        
        self.loop.run_until_complete(self.create_db_pool())
    
    async def create_db_pool(self):
        self.db = await asyncpg.create_pool(database = "CoolBot", user = "postgres", password = password)