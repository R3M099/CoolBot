import discord
from discord.ext import commands
from datetime import datetime
import asyncio

class Poll(commands.Cog):
    """Contains poll command"""

    def __init__(self, bot : commands.Bot):
        self.bot = bot
        
    @commands.command()
    async def poll(self, ctx, choice_1, choice_2, *, topic):
        """Start a poll of your choice"""
        e = discord.Embed(title = topic, description = f":one: {choice_1} \n\n :two: {choice_2}", color = ctx.author.color, timestamp = datetime.utcnow())
        e.set_footer(text = f"Poll created by {ctx.author.name}")
        e.set_thumbnail(url = ctx.guild.icon_url)
        message = await ctx.send(embed = e)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        
        await asyncio.sleep(3600)

        new_message = await ctx.fetch_message(message.id)
        first_choice = await new_message.reactions[0].users().flatten()
        second_choice = await new_message.reactions[1].users().flatten()

        result = "TIE"
        if len(first_choice) > len(second_choice):
            result = choice_1
        
        elif len(second_choice) > len(first_choice):
            result = choice_2

        e = discord.Embed(title = topic, description = f"Result : {result}", color = ctx.author.color, timestamp = datetime.utcnow())
        e.set_footer(text = f"{choice_1} || {choice_2}")

        await new_message.edit(embed = e)

def setup(bot):
    bot.add_cog(Poll(bot))