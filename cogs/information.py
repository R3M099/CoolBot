import discord
from discord.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from afks import afks
import requests

""
urls = {"warzone":"https://wallpaperaccess.com/full/930562.jpg",
        "maskcodes":"https://www.zastavki.com/pictures/1280x720/2019Creative_Wallpaper_Gas_mask_with_a_numerical_code_background_136603_26.jpg",
        "mikasa":"https://images.wallpapersden.com/image/download/anime-shingeki-no-kyojin-mikasa-ackerman_ZmZna26UmZqaraWkpJRmZ21lrWxnZQ.jpg",
        "devilmay":"https://images.wallpapersden.com/image/download/devil-may-cry-5-4k_a2hubWyUmZqaraWkpJRmZ21lrWxnZQ.jpg",
        "binary":"https://wallpaperaccess.com/full/4220753.jpg",
        "default":"https://images.hdqwalls.com/download/anime-sunset-scene-b8-1280x720.jpg",
        "blocks":"https://cdn.wallpapersafari.com/77/30/wKc3Jy.jpg",
        "pubg":"https://hdqwalls.com/download/pubg-android-game-4k-eh-1280x720.jpg",
        "naruto":"https://images.hdqwalls.com/download/kakashi-hatake-anime-4k-yk-1280x720.jpg"}


def circle(pfp, size = (215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill = 255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)

    return pfp

class Information(commands.Cog):
    """Information commands for knowing more about the user and the server."""

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    async def add(self, id, amount = 0):
        user = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userid = $1", id)
        await self.bot.db.execute("UPDATE economy SET money = $1 WHERE userid = $2", user[1] + amount, id)
    
    async def get(self, id):
        user = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userid = $1", id)
        if user is None:
            return None
        return user[1]
    
    async def check(self, id):
        user = await self.bot.db.fetch("SELECT * FROM economy WHERE userid = $1", id)
        if not user:
            return await self.bot.db.execute("INSERT INTO economy (userid, money, bgs) VALUES ($1, $2, $3)", id, 0, ["default"])
    
    async def available(self, id):
        urls = await self.bot.db.fetchrow("SELECT bgs FROM economy WHERE userid = $1", id)
        if urls is None:
            await self.bot.db.execute("UPDATE economy SET bgs = $1 WHERE userid = $2", ["default"], id)
            return ["default"]
        return urls[0]
    
    async def update(self, id, back):
        urls = await self.available(id)
        if urls is None:
            urls = []
        if back in urls:
            urls.remove(back)
        urls.insert(0, back)
        await self.bot.db.execute("UPDATE economy SET bgs = $1 WHERE userid = $2", urls, id)
    
    @commands.command(aliases = ["ui", "profile", "whois"])
    async def userinfo(self, ctx, member : discord.Member = None):
        """Gives the information about the member"""
        if not member:
            member = ctx.author
        
        await self.check(member.id)

        created_at = member.created_at.strftime("%a, %#d \n%B %Y")
        joined_at = member.joined_at.strftime("%a, %#d \n%B %Y")
        money = await self.get(member.id)
        top_role = member.top_role.name
        ava = await self.available(member.id)
        status = str(member.status).upper()
        url = urls[ava[0]]
        background = Image.open(requests.get(url, stream = True).raw)

        asset = member.avatar_url_as(size = 256)
        guildnote = member.guild.icon_url_as(size = 256)
        data = BytesIO(await asset.read())
        gdata = BytesIO(await guildnote.read())
        pfp = Image.open(data).convert("RGB")
        logo = Image.open(gdata).convert("RGB")
        pfp = circle(pfp, (255, 255))
        logo = circle(logo, (180, 180))

        name = str(member)
        if len(top_role) > 12:
            top_role = top_role[:13]
        if len(name) > 20:
            name = name[:21]

        background = Image.open(requests.get(url, stream = True).raw)
        main = Image.open("./Assets/images/base.png")
        bg = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        bg.paste(background, (0,0))
        bg.paste(main, (0,0), mask=main)
        draw = ImageDraw.Draw(bg)
        myFont = ImageFont.truetype('./Assets/fonts/bahnschrift.ttf', 45)
        draw.text((570,270),name, font = myFont, fill = (0, 0, 0), stroke_width=3, stroke_fill=(255, 255, 255))
        myFont = ImageFont.truetype('./Assets/fonts/bahnschrift.ttf', 35)
        myFont2 = ImageFont.truetype('./Assets/fonts/bahnschrift.ttf', 30)
        myFont3 = ImageFont.truetype('./Assets/fonts/bahnschrift.ttf', 25)
        draw.text((850, 550),created_at, font = myFont2, fill = (0,0,0), stroke_width = 2, stroke_fill=(255, 255, 255))
        draw.text((850, 425),joined_at, font = myFont2, fill = (0,0,0), stroke_width = 2, stroke_fill=(255, 255, 255))
        draw.text((150, 555),str(money), font = myFont, fill = (0,0,0), stroke_width = 2, stroke_fill=(255, 255, 255))
        draw.text((122, 435),str(member.id), font = myFont3, fill = (0,0,0), stroke_width = 2, stroke_fill=(255 ,255, 255))
        draw.text((500, 555),top_role,font = myFont,fill = (0,0,0), stroke_width = 2, stroke_fill=(255, 255, 255))
        draw.text((500, 425),status,font = myFont,fill = (0,0,0), stroke_width = 2, stroke_fill=(255, 255, 255))   
        bg.paste(pfp, (275, 102), pfp)
        bg.paste(logo, (25, 25), logo)

        with BytesIO() as a:
            bg.save(a, "PNG")
            a.seek(0)
            await ctx.send(file = discord.File(a, filename = "profile.png"))
        
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        if ava[0] == "default":
            await ctx.send(f"{member.mention}, you can also buy and set different background image other than the default one. \n Type `{prefix}shop` to see the list of all the background images available and `{prefix}setbg <bg_name>` to set a different background.")

    @commands.command(aliases = ["si"])
    async def serverinfo(self, ctx):
        """Gives the information about the server"""
        e = discord.Embed(title = f"ID : {ctx.guild.id}", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Verification Level", value = ctx.guild.verification_level, inline = False)
        e.add_field(name = "Region", value = ctx.guild.region, inline = False)
        e.add_field(name = "Members", value = ctx.guild.member_count, inline = False)
        e.add_field(name = "Server Owner", value = f"{ctx.guild.owner} [{ctx.guild.owner_id}]", inline = False)
        e.add_field(name = "Created On", value = ctx.guild.created_at.__format__("%A, %B %d %Y @ %X %p"), inline = False)
        e.add_field(name = "Channels", value = len(ctx.guild.text_channels), inline = False)
        e.set_thumbnail(url = ctx.guild.icon_url)
        e.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
        await ctx.send(embed = e)

    @commands.command(aliases = ["switch"])
    async def setbg(self, ctx, back):
        """Set background image for your profile"""
        back = back.lower()
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        urlname = await self.available(ctx.author.id)

        if back in urls.keys():
            if back in urlname:
                await self.update(ctx.author.id, back)
                await ctx.send("Background Image for your profile has been successfully changed!")
            else:
                await ctx.send(embed = discord.Embed(title = "Error Occured", description = f"You don't have any background image named `{back}`.\n Type `{prefix}shop` for more info.", color = discord.Color.random(), timestamp = datetime.utcnow()))
        else:
            await ctx.send(embed = discord.Embed(title = "Error Occured", description = f"There is no such background image available (atleast i doubt it). Please recheck the name and try again. \n Type {prefix}shop for more info.", color = discord.Color.random(), timestamp = datetime.utcnow()))
    
    @commands.command(aliases = ["backgrounds", "back", "background"])
    async def bg(self, ctx):
        """See all the available background images available for your profile"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        backgrounds = await self.available(ctx.author.id)
        names = ", ".join(backgrounds)
        e = discord.Embed(title = "Background Images availabel for your profile : ", description = names, color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Active Background : ", value = backgrounds[0], inline = False)
        e.add_field(name = "Changing background image help : ", value = f"Type `{prefix}setbg <bg_name>` or `{prefix}switch <bg_name>` to change your bg image", inline = False)
        c = 1
        await ctx.send(embed = e)
        for i in backgrounds:
            await ctx.send(f"{c}) {i}\n{urls[i]}", delete_after = 6)
            c += 1
    
    @commands.command()
    async def afk(self, ctx, *, reason = "No reason provided"):
        """Set yourself AFK for some time."""
        member = ctx.author

        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick = f"[AFK] {member.display_name}")
            except:
                pass
        
        afks[member.id] = reason
        
        e = discord.Embed(title = ":zzz: Member AFK", description = f"{member.mention} has gone AFK", color = member.color, timestamp = datetime.utcnow())
        e.set_thumbnail(url = member.avatar_url)
        e.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
        e.add_field(name = "AFK note:", value = reason)

        await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(Information(bot))