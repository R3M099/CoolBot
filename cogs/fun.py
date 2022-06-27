import discord
from discord.ext import commands
from datetime import datetime
from aiohttp import request

class Fun(commands.Cog):
    """Commands to uplift your mood"""
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pjoke(self, ctx):
        """Sends a funny programming related joke"""
        pjoke_url = "https://sv443.net/jokeapi/v2/joke/Programming?blacklistFlags=nsfw&type=twopart"
        # pjoke_url = "https://backend-omega-seven.vercel.app/api/getjoke"
        async with request("GET", pjoke_url, headers = {}) as response:
            if response.status == 200:
                data = await response.json()
                e = discord.Embed(title = data["setup"], description = data["delivery"], color = ctx.author.color, timestamp = datetime.utcnow())

                await ctx.send(embed = e)
            else:
                await ctx.send(f"API returned a {response.status} status")
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def xkcd(self, ctx, number : int):
        """Sends a webcomic containing mathematical, scientific, life related humors"""
        xkcd_url = f"https://xkcd.com/{number}/info.0.json"

        async with request("GET", xkcd_url, headers = {}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["img"]

                e = discord.Embed(title = data["title"], description = data["alt"], color = ctx.author.color, timestamp = datetime.utcnow())
                e.set_author(name = f"{ctx.author.name}", icon_url = ctx.author.avatar_url)
                e.add_field(name = "Released in - ", value = data["year"])
                if image_link is not None:
                    e.set_image(url = image_link)
                
                await ctx.send(embed = e)
            
            else:
                await ctx.send(f"API returned a {response.status} status")
    

def setup(bot):
    bot.add_cog(Fun(bot))