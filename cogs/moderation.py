#from sqlite3 import Timestamp
import discord
from discord.ext import commands
from datetime import datetime

#from hikari import Embed

class Moderation(commands.Cog):
    """Moderation commands to maintain the decorum of the server"""

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    async def warn_log(self, guild_id, member_id):
        data = await self.bot.db.fetchrow("SELECT * FROM warnlogs WHERE guild_id = $1 AND member_id = $2", guild_id, member_id)

        if not data:
            return []
        
        return data
    
    async def warn_entry(self, guild_id, member_id, reason, time):
        data = await self.warn_log(guild_id, member_id)
        if data == []:
            await self.bot.db.execute("INSERT INTO warnlogs (guild_id, member_id, warns, times) VALUES ($1, $2, $3, $4)", guild_id, member_id, [reason], [time])
            return
        
        warns = data[2]
        times = data[3]

        if not warns:
            warns = [reason]
            times = [time]
        else:
            warns.append(reason)
            times.append(time)

        await self.bot.db.execute("UPDATE warnlogs SET times = $1, warns = $2 WHERE guild_id = $3 AND member_id = $4", times, warns, guild_id, member_id)
    
    async def del_warn(self, guild_id, member_id, index):
        data = await self.warn_log(guild_id, member_id)
        if len(data[2]) >= 1:
            data[2].remove(data[2][index])
            data[3].remove(data[3][index])
            return await self.bot.db.execute("UPDATE warnlogs SET warns = $1, times = $2 WHERE guild_id = $3 AND member_id = $4", data[2], data[3], guild_id, member_id)
        
        await self.bot.db.execute("DELETE FROM warnlogs WHERE guild_id = $1 AND member_id = $2", guild_id, member_id)
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = "No reason provided"):
        """Ban a member from the server"""

        id = await self.bot.db.fetchrow("SELECT modlogs FROM guilds WHERE guildid = $1", ctx.guild.id)
            
        if not id[0]:
            pass
        
        log = self.bot.get_channel(id[0])

        e = discord.Embed(title = "Member Banned", description = f"{member.mention} has been banned from {ctx.guild.name}", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Resposible Mod", value = ctx.author.mention, inline = False)
        e.add_field(name = "Reason Provided", value = reason, inline = False)

        try:
            await member.ban(reason = reason)
            await ctx.send(f"**{member.name}** has been banned by **{ctx.author.name}**")
            await log.send(embed = e)
        
        except:
            await ctx.send(embed = discord.Embed(title = "Missing Permissions", description = "The user/bot doesn't have the required permissions to ban the member.", color = discord.Color.red(), timestamp = datetime.utcnow()))

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason = "No reason provided"):
        """Kicks a member from the server"""

        id = await self.bot.db.fetchrow("SELECT modlogs FROM guilds WHERE guildid = $1", ctx.guild.id)
            
        if not id[0]:
            pass
        
        log = self.bot.get_channel(id[0])

        e = discord.Embed(title = "Member Kicked", description = f"{member.mention} has been kicked from {ctx.guild.name}", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Resposible Mod", value = ctx.author.mention, inline = False)
        e.add_field(name = "Reason Provided", value = reason, inline = False)

        try:
            await member.kick(reason = reason)
            await ctx.send(f"**{member.name}** has been kicked by **{ctx.author.name}**")
            await log.send(embed = e)
        
        except:
            await ctx.send(embed = discord.Embed(title = "Missing Permissions", description = "The user/bot doesn't have the required permissions to kick the member.", color = discord.Color.red(), timestamp = datetime.utcnow()))

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member_id):
        """Unbans a banned member from the server"""

        id = await self.bot.db.fetchrow("SELECT modlogs FROM guilds WHERE guildid = $1", ctx.guild.id)
            
        if not id[0]:
            pass
        
        log = self.bot.get_channel(id[0])

        user = await self.bot.fetch_user(member_id)
        e = discord.Embed(title = "Member Unbanned", description = f"{user.name} has been unbanned from {ctx.guild.name}", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Resposible Mod", value = ctx.author.mention, inline = False)

        try:
            await ctx.guild.unban(user)
            await ctx.send(f"**{user.name}** has been unbanned by **{ctx.author.name}**")
            await log.send(embed = e)
            return
        
        except discord.NotFound:
            await ctx.send(embed = discord.Embed(title = "Member not found", color = discord.Color.red(), timestamp = datetime.utcnow()))
            return
        
        #await ctx.send(embed = discord.Embed(title = "Missing Permissions", description = "The user/bot doesn't have the required permissions to unban the member.", color = discord.Color.red(), timestamp = datetime.utcnow()))

    @commands.command(aliases = ["purge"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount : int = 2):
        """Purges the unwanted chat"""
        if amount < 1:
            await ctx.send("The number of messages to purge should be more than one.")
            return

        try:
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send(f"{amount} messages have been deleted.", delete_after = 5)
        
        except:
            await ctx.send("You don't have the required permissions to clear the chat.")
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member : discord.Member, *, reason = "No reason provided"):
        """Warns a member for causing nuissance in the server"""
        id = await self.bot.db.fetchrow("SELECT modlogs FROM guilds WHERE guildid = $1", ctx.guild.id)
            
        if not id[0]:
            pass
        
        log = self.bot.get_channel(id[0])

        if member == ctx.author or member == self.bot.user:
            return await ctx.send("You can't warn yourself or the bot.")
        
        if not ctx.author.top_role.position > member.top_role.position:
            return await ctx.send("You can't warn a member who is higher in position or at the same level as you.")
        
        await self.warn_entry(ctx.guild.id, member.id, reason, ctx.message.created_at.timestamp())
        await ctx.send(f"**{member.name}** has been warned by **{ctx.author.name}** for reason : {reason}")

        data = await self.warn_log(ctx.guild.id, member.id)
        count = len(data[3])

        e = discord.Embed(title = f"Warned by {ctx.author}", color = ctx.author.color, timestamp = datetime.utcnow())
        e.add_field(name = "Reason", value = reason)
        e.add_field(name = "Total warns", value = f"**{count}** warns \n More than 5 warns in a week can have severe consequences!")
        e.set_thumbnail(url = ctx.guild.icon_url)

        await log.send(embed = e)

        try:
            await member.send(embed = e)
        except:
            pass
    
    @commands.command()
    async def warns(self, ctx, member : discord.Member = None):
        """Displays the number of warns of a member"""
        if not member:
            member = ctx.author
        
        data = await self.warn_log(ctx.guild.id, member.id)
        if not data or not data[3]:
            return await ctx.send("This user has no warns.")
        
        e = discord.Embed(title = f"Warns of {member.display_name}({member.id})", description = f"Total warns : `{len(data[2])}`", color = member.color, timestamp = datetime.utcnow())
        e.set_thumbnail(url = member.avatar_url)
        for i in range(len(data[2])):
            #timestamp = datetime.fromtimestamp(data[3][i]).strftime("%c")
            reason = data[2][i]
            e.add_field(name = f"Reason : {reason}", value = f"Warn ID : {data[3][i]}", inline = False)
        
        e.set_footer(text = "Warns will be cleared automatically after every month.")
        await ctx.send(embed = e)
    
    @commands.command()
    async def delwarn(self, ctx, member : discord.Member, warn_id : float):
        """Deletes the warns of a member"""
        data = await self.warn_log(ctx.guild.id, member.id)
        if data == []:
            await ctx.send("This user has no warns.")
        if data[3] and warn_id in data[3]:
            index = data[3].index(warn_id)
            await self.del_warn(ctx.guild.id, member.id, index)
            return await ctx.send(f":white_check_mark: Successfully deleted one warning for {member.display_name}")
        else:
            return await ctx.send(":negative_squared_cross_mark: No warn entry with the corresponding user found.")



def setup(bot):
    bot.add_cog(Moderation(bot))