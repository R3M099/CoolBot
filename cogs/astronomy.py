from email.mime import image
import json
from random import randint
from secrets import choice
import discord
from discord.ext import commands
from datetime import datetime
from aiohttp import request
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

apod_url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
curiosity_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={API_KEY}"
opportunity_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/latest_photos?api_key={API_KEY}"
spirit_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/latest_photos?api_key={API_KEY}"
perseverance_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/latest_photos?api_key={API_KEY}"

class Astronomy(commands.Cog):
    """If you love space, then these commands are for you."""

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def apod(self, ctx):
        """Sends a beautiful image of space (Changes every 24 hours)"""

        async with request("GET", apod_url, headers = {}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["hdurl"]

                e = discord.Embed(title = data["title"], description = data["explanation"], color = discord.Color.random(), timestamp = datetime.utcnow())
                e.set_author(name = f"{ctx.author.name}", icon_url = ctx.author.avatar_url)

                if image_link is not None:
                    e.set_image(url = image_link)
                
                await ctx.send(embed = e)
            else:
                #image_link = None
                await ctx.send(f"API returned a {response.status} status")
    
    @commands.command(aliases = ["marsimage", "marspic"])
    #@commands.cooldown(1, 20, commands.BucketType.user)
    async def mars(self, ctx, rover_name : str):
        """Searches the database of Curiosity, Opportunity, Perseverance, and Spirit for amazing images of the martian landscape."""

        #rovers = [curiosity_url, opportunity_url, spirit_url, perseverance_url]
        # if rover_name is None:
        #     await ctx.send("Please provide the name of the rover!")
        
        if rover_name == "curiosity":
            r = requests.get(curiosity_url)
            mars_dict = json.loads(r.content)
            latest_dict = choice(mars_dict["latest_photos"])

            marsDay = latest_dict["sol"]
            cameraName = latest_dict["camera"]["full_name"]
            imageLink = latest_dict["img_src"]
            earthDate = latest_dict["earth_date"]

            e = discord.Embed(title = "Here is a beautiful image from the Curiosity Rover", color = discord.Color.random(), timestamp = datetime.utcnow())
            e.set_author(name = "NASA", icon_url = "https://1000logos.net/wp-content/uploads/2017/03/NASA-Logo.png")
            e.set_image(url = imageLink)
            e.add_field(name = "Mars Day (sol)", value = marsDay, inline = True)
            e.add_field(name = "Earth day", value = earthDate, inline = True)
            e.add_field(name = "Camera used", value = cameraName, inline = True)

            await ctx.send(embed = e)
        
        elif rover_name == "opportunity":
            r = requests.get(opportunity_url)
            mars_dict = json.loads(r.content)
            latest_dict = choice(mars_dict["latest_photos"])

            marsDay = latest_dict["sol"]
            cameraName = latest_dict["camera"]["full_name"]
            imageLink = latest_dict["img_src"]
            earthDate = latest_dict["earth_date"]

            e = discord.Embed(title = "Here is a beautiful image from the Opportunity Rover", color = discord.Color.random(), timestamp = datetime.utcnow())
            e.set_author(name = "NASA", icon_url = "https://1000logos.net/wp-content/uploads/2017/03/NASA-Logo.png")
            e.set_image(url = imageLink)
            e.add_field(name = "Mars Day (sol)", value = marsDay, inline = True)
            e.add_field(name = "Earth day", value = earthDate, inline = True)
            e.add_field(name = "Camera used", value = cameraName, inline = True)

            await ctx.send(embed = e)
        
        elif rover_name == "spirit":
            r = requests.get(spirit_url)
            mars_dict = json.loads(r.content)
            latest_dict = choice(mars_dict["latest_photos"])

            marsDay = latest_dict["sol"]
            cameraName = latest_dict["camera"]["full_name"]
            imageLink = latest_dict["img_src"]
            earthDate = latest_dict["earth_date"]

            e = discord.Embed(title = "Here is a beautiful image from the Spirit Rover", color = discord.Color.random(), timestamp = datetime.utcnow())
            e.set_author(name = "NASA", icon_url = "https://1000logos.net/wp-content/uploads/2017/03/NASA-Logo.png")
            e.set_image(url = imageLink)
            e.add_field(name = "Mars Day (sol)", value = marsDay, inline = True)
            e.add_field(name = "Earth day", value = earthDate, inline = True)
            e.add_field(name = "Camera used", value = cameraName, inline = True)

            await ctx.send(embed = e)
        
        elif rover_name == "perseverance":
            r = requests.get(perseverance_url)
            mars_dict = json.loads(r.content)
            latest_dict = choice(mars_dict["latest_photos"])

            marsDay = latest_dict["sol"]
            cameraName = latest_dict["camera"]["full_name"]
            imageLink = latest_dict["img_src"]
            earthDate = latest_dict["earth_date"]

            e = discord.Embed(title = "Here is a beautiful image from the Perseverance Rover", color = discord.Color.random(), timestamp = datetime.utcnow())
            e.set_author(name = "NASA", icon_url = "https://1000logos.net/wp-content/uploads/2017/03/NASA-Logo.png")
            e.set_image(url = imageLink)
            e.add_field(name = "Mars Day (sol)", value = marsDay, inline = True)
            e.add_field(name = "Earth day", value = earthDate, inline = True)
            e.add_field(name = "Camera used", value = cameraName, inline = True)

            await ctx.send(embed = e)
        
        else:
            await ctx.send("There are no images to show :slight_frown:")
        

def setup(bot):
    bot.add_cog(Astronomy(bot))