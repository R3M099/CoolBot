from os import name
import discord
from discord.ext import commands
import random
from datetime import datetime

class Logs(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.bot:
            return
        try:
            id = await self.bot.db.fetchrow("SELECT userlog FROM guilds WHERE guildid = $1", after.guild.id)
            
            if not id[0]:
                pass
            
            log = self.bot.get_channel(id[0])

            old_roles = " ".join([role.mention for role in before.roles])
            new_roles = " ".join([role.mention for role in after.roles])

            e = discord.Embed(title = "Member Update", color = discord.Color.random(), timestamp = datetime.utcnow())

            def fun(state):
                activity = ""
                if isinstance(state.activities, tuple):
                    for i in state.activities:
                        try:
                            activity = activity+ i.name+" "
                        except:
                            pass

                        try:
                            activity = activity+"**"+i.title+"**"
                        except:
                            pass

                        activity += "\n"
                
                else:
                    activity = state.activities[0]
                
                if activity == "":
                    activity = "None"
                
                return activity
            
            e.set_author(name = after, icon_url = after.avatar_url)

            if str(before.status).upper() != str(after.status).upper():
                e.add_field(name = "Old Status : ", value = f"{str(before.status).upper()}")
                e.add_field(name = "New Status : ", value = f"{str(after.status).upper()}")
                return
            
            elif fun(before) != fun(after):
                e.add_field(name = "Old Activity : ", value = f"{fun(before)}")
                e.add_field(name = "New Activity : ", value = f"{fun(after)}")
                return
            
            elif before.display_name != after.display_name:
                e.add_field(name = "Old Nickname : ", value = f"{before.display_name}")
                e.add_field(name = "New Nickname : ", value = f"{after.display_name}")
            
            elif old_roles != new_roles:
                e.add_field(name = "Old Roles : ", value = f"{old_roles}")
                e.add_field(name = "New Roles : ", value = f"{new_roles}")
            
            else:
                return
            
            await log.send(embed = e)
        
        except:
            pass
    
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.bot:
            return
        
        try:
            id = await self.bot.db.fetchrow("SELECT userlog FROM guilds WHERE guildid = $1", after.guild.id)
            
            if not id[0]:
                pass
            
            log = self.bot.get_channel(id[0])

            e = discord.Embed(title = "User Update", description = "Avatar change", color = discord.Color.random(), timestamp = datetime.utcnow())
            
            if before.avatar_url != after.avatar_url:
                e.set_author(name = f"{after.display_name}", icon_url = before.avatar_url)
                e.set_thumbnail(url = after.avatar_url)
            else:
                return
            
            await log.send(embed = e)
        
        except:
            pass

    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        id = await self.bot.db.fetchrow("SELECT messagelog FROM guilds WHERE guildid = $1", message.guild.id)

        if not id[0]:
            return
        
        if message.author.bot:
            return
        
        log = self.bot.get_channel(id[0])

        e = discord.Embed(description = f"Message deleted in <#{message.channel.id}>", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Message", value = message.content, inline = False)
        e.set_author(name = str(message.author), icon_url = message.author.avatar_url)
        e.set_footer(text = f"User ID : {message.author.id}")
        e.set_thumbnail(url = "https://icons.iconarchive.com/icons/cornmanthe3rd/plex/512/System-recycling-bin-full-icon.png")

        await log.send(embed = e)
    
    @commands.Cog.listener()
    async def on_message_edit(self, old, new):
        id = await self.bot.db.fetchrow("SELECT messagelog FROM guilds WHERE guildid = $1", old.guild.id)

        if not id[0]:
            return
        
        if old.author.bot:
            return
        
        log = self.bot.get_channel(id[0])

        e = discord.Embed(description = f"Message edited in <#{old.channel.id}> \n **[Jump to message]({new.jump_url})**", color = discord.Color.random(), timestamp = datetime.utcnow())
        e.add_field(name = "Old Message", value = old.content, inline = False)
        e.add_field(name = "New Message", value = new.content, inline = False)
        e.set_author(name = str(old.author), icon_url = old.author.avatar_url)
        e.set_footer(text = f"User ID : {old.author.id}")
        e.set_thumbnail(url = "https://th.bing.com/th/id/R66dbcbb7f70864efa5e4e8097e865a28?rik=KbhIVKRoP5CCLw&riu=http%3a%2f%2fwww.recycling.com%2fwp-content%2fuploads%2f2016%2f06%2frecycling-symbol-icon-outline-solid-dark-green.png&ehk=uUs07SqPyEepr2jBZhiGSUkO1QbzTCvEobnhAM%2fddU8%3d&risl=&pid=ImgRaw")

        await log.send(embed = e)

def setup(bot):
    bot.add_cog(Logs(bot))