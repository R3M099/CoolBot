from webbrowser import get
import discord
from discord.ext import commands
import asyncpg
from datetime import datetime

class Utility(commands.Cog):
    
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.command(aliases = ["setprefix"])
    @commands.has_permissions(administrator = True)
    async def prefix(self, ctx, new_prefix):
        """Change the prefix of the server according to your needs."""
        await self.bot.db.execute("UPDATE guilds SET prefix = $1 WHERE guildid = $2", new_prefix, ctx.guild.id)
        await ctx.send(f"The prefix of the server has been set to `{new_prefix}`")
    
    @commands.command(aliases = ["userlog"])
    @commands.has_permissions(administrator = True)
    async def setuserlog(self, ctx, channel : discord.TextChannel):
        """Set a log channel to get the user logs for the server"""
        await self.bot.db.execute("UPDATE guilds SET userlog = $1 WHERE guildid = $2", channel.id, ctx.guild.id)
        e = discord.Embed(title = "User Log Channel Updated", description = f"Log channel has been set to {channel.mention}", color = discord.Color.random(), timestamp = datetime.utcnow())
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["remove_user_log"])
    @commands.has_permissions(administrator = True)
    async def deluserlog(self, ctx):
        """Remove the existing user log channel for the server"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        await self.bot.db.execute("UPDATE guilds SET userlog = $1 WHERE guildid = $2", None, ctx.guild.id)
        e = discord.Embed(title = "Log Channel Removed", description = f"User logs for **{ctx.guild.name}** has been turned off", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.set_footer(text = f"Type {prefix}setuserlog <channel_name> to start logging user activity again")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["messagelog"])
    @commands.has_permissions(administrator = True)
    async def setmessagelog(self, ctx, channel : discord.TextChannel):
        """Set a log channel to get the message logs for the server"""
        await self.bot.db.execute("UPDATE guilds SET messagelog = $1 WHERE guildid = $2", channel.id, ctx.guild.id)
        e = discord.Embed(title = "Message Log Channel Updated", description = f"Log channel has been set to {channel.mention}", color = discord.Color.random(), timestamp = datetime.utcnow())
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["remove_message_log"])
    @commands.has_permissions(administrator = True)
    async def delmessagelog(self, ctx):
        """Remove the existing message log channel for the server"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        await self.bot.db.execute("UPDATE guilds SET messagelog = $1 WHERE guildid = $2", None, ctx.guild.id)
        e = discord.Embed(title = "Log Channel Removed", description = f"Message logs for **{ctx.guild.name}** has been turned off", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.set_footer(text = f"Type {prefix}setmessagelog <channel_name> to start logging message activity again")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["modlog"])
    @commands.has_permissions(administrator = True)
    async def setmodlog(self, ctx, channel : discord.TextChannel):
        """Set a log channel to get the mod logs for the server"""
        await self.bot.db.execute("UPDATE guilds SET modlogs = $1 WHERE guildid = $2", channel.id, ctx.guild.id)
        e = discord.Embed(title = "Mod Log Channel Updated", description = f"Log channel has been set to {channel.mention}", color = discord.Color.random(), timestamp = datetime.utcnow())
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["remove_mod_log"])
    @commands.has_permissions(administrator = True)
    async def delmodlog(self, ctx):
        """Remove the existing mod log channel for the server"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        await self.bot.db.execute("UPDATE guilds SET modlogs = $1 WHERE guildid = $2", None, ctx.guild.id)
        e = discord.Embed(title = "Log Channel Removed", description = f"Mod logs for **{ctx.guild.name}** has been turned off", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.set_footer(text = f"Type {prefix}setmodlog <channel_name> to start logging mod activity again")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["welcomechannel"])
    @commands.has_permissions(administrator = True)
    async def setwelcome(self, ctx, channel : discord.TextChannel):
        """Sets a welcome channel for the server"""
        await self.bot.db.execute("UPDATE guilds SET welcome = $1 WHERE guildid = $2", channel.id, ctx.guild.id)
        e = discord.Embed(title = "Welcome Channel Updated", description = f"Welcome channel has been set to {channel.mention}", color = discord.Color.random(), timestamp = datetime.utcnow())
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["removewelcome"])
    @commands.has_permissions(administrator = True)
    async def delwelcome(self, ctx):
        """Removes the existing welcome channel of the server"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        await self.bot.db.execute("UPDATE guilds SET welcome = $1 WHERE guildid = $2", None, ctx.guild.id)
        e = discord.Embed(title = "Welcome Channel Removed", description = f"Welcome channel for **{ctx.guild.name}** has been turned off", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.set_footer(text = f"Type {prefix}setwelcome <channel_name> to start welcoming members again")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["reportbug"])
    async def bug(self, ctx, *, bug):
        """Report a bug to the bot developer"""
        owner = await self.bot.fetch_user(537634097137188875)
        e = discord.Embed(title = "Bug Report", description = f"{bug} \n Reported by **{ctx.author.name}** from **{ctx.guild.name}**", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        try:
            await owner.send(embed = e)
            await ctx.send("Bug has been successfully submitted to the developer :slight_smile:", delete_after = 5)
        except Exception as e:
            await ctx.send(f"Bug could not be delivered, try again later \n {e}", delete_after = 5)

def setup(bot):
    bot.add_cog(Utility(bot))