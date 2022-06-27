import discord
from discord.ext import commands, tasks
from discord.ext.commands import errors
from afks import afks
from discord.utils import get
from datetime import datetime

def remove(afk):
    if "[AFK]" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

invites = {}

def find_invite_by_code(invite_list, code):
        for inv in invite_list:
            if inv.code == code:
                return inv

#bot = commands.Bot()

class Event(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    async def add(self, id, amount = 0):
        bal = await self.bot.db.fetchrow("SELECT money FROM economy WHERE userid = $1", id)
        await self.bot.db.execute("UPDATE economy SET money = $1 WHERE userid = $2", amount + bal[0], id)
    
    async def check(self, id):
        user = await self.bot.db.fetch("SELECT * FROM economy WHERE userid = $1", id)
        if not user:
            await self.bot.db.execute("INSERT INTO economy (userid, money, inventory, bgs) VALUES ($1, $2, $3, $4)", id, 0, [], ["default"])
            
    # @tasks.loop(hours = 24)
    # async def clean_warns(self):
    #     current_time = datetime.now()
    #     data = await self.bot.db.fetch("SELECT * FROM warnlogs")
    #     for row in data:
    #         if not row[3]:
    #             await self.bot.db.execute("DELETE FROM warnlogs WHERE guild_id = $1 AND member_id = $2", row[0], row[1])
    #             continue
    #         for time in row[3]:
    #             timestamp = datetime.fromtimestamp(time)
    #             diff = current_time - timestamp
    #             if diff.days >= 0:
    #                 index = row[3].index(time)
    #                 if len(row[3]) == 1:
    #                     await self.bot.db.execute("DELETE FROM warnlogs WHERE guild_id = $1 AND member_id = $2", row[0], row[1])
    #                 else:
    #                     row[2].remove(row[2][index])
    #                     row[3].remove(row[3][index])
    #                     await self.bot.db.execute("UPDATE warnlogs SET warns = $1, times = $2 WHERE member_id = $3 AND guild_id = $4", row[2], row[3], row[1], row[0])                        
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS warnlogs (guild_id BIGINT, member_id BIGINT, warns TEXT[], times DECIMAL[])")
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS economy (userid BIGINT NOT NULL, money BIGINT, inventory TEXT[], bgs TEXT[])")
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS guilds (guildid BIGINT NOT NULL, prefix TEXT, messagelog BIGINT, userlog BIGINT, modlogs BIGINT, welcome BIGINT)")
        # await self.bot.db.execute("CREATE TABLE IF NOT EXISTS users (userid BIGINT NOT NULL, guildid BIGINT, xp INT, level INT)")
        # await self.bot.db.execute("ALTER TABLE economy ADD COLUMN IF NOT EXISTS userid BIGINT NOT NULL")
        # await self.bot.db.execute("ALTER TABLE economy ADD COLUMN IF NOT EXISTS money BIGINT")

        for guild in self.bot.guilds:
            invites[guild.id] = await guild.invites()

        await self.bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = "the souls of the damned"))

        print("The bot is ready!")
        # await self.clean_warns.start()
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        invites_before_join = invites[member.guild.id]
        invites_after_join = await member.guild.invites()

        id = await self.bot.db.fetchrow("SELECT welcome FROM guilds WHERE guildid = $1", member.guild.id)

        if not id[0]:
            pass

        welcome = self.bot.get_channel(id[0])

        for invite in invites_before_join:
            if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
                await self.check(invite.inviter.id)

                await welcome.send(f"**{invite.inviter.name}** invited **{member.name}** to **{member.guild.name}**.\n Thankyou and here is 1000 coins on behalf of {member.guild.name} staffs :slight_smile:")
                await self.add(invite.inviter.id, 1000)
                # print(f"Member {member.name} Joined")
                # print(f"Invite Code : {invite.code}")
                # print(f"Inviter : {invite.inviter}")

                invites[member.guild.id] = invites_after_join
                # print(invites)
                return
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        invites[member.guild.id] = await member.guild.invites()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.", delete_after = 5)
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("Command does not exist.\n type help for more info.", delete_after = 5)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Data type passed is invalid.\n `{str(error)}`")
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Command is on cooldown for {error.retry_after:,.0f} seconds. Please try again later!")
        else:
            raise error
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick = remove(message.author.display_name))
            except:
                pass

            await message.channel.send(f"Welcome back {message.author.display_name}! I removed your AFK status.")
        
        for id, reason in afks.items():
            member = get(message.guild.members, id = id)
            if(message.reference and member == (message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                await message.reply(f"{member.name} is AFK currently.\n AFK Note : {reason}.")

def setup(bot):
    bot.add_cog(Event(bot))