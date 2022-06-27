from secrets import choice
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from random import randint, random
import random
from PIL import ImageDraw, ImageFont, Image
from io import BytesIO
#from bot import get_prefix

with open("typingtext.txt", "r") as f:
    sentences = [i.replace("\n", "") or i for i in f.readlines()]

shopping = [{"name":"warzone","price" : 20000 , "description" : "[Click HERE](https://wallpaperaccess.com/full/930562.jpg) for Image Preview" } ,
            {"name":"maskcodes","price" : 20000 , "description" : "[Click HERE](https://www.zastavki.com/pictures/1280x720/2019Creative_Wallpaper_Gas_mask_with_a_numerical_code_background_136603_26.jpg) for Image Preview" },
            {"name":"mikasa","price" : 15000 , "description" : "[Click HERE](https://images.wallpapersden.com/image/download/anime-shingeki-no-kyojin-mikasa-ackerman_ZmZna26UmZqaraWkpJRmZ21lrWxnZQ.jpg) for Image Preview" } ,
            {"name":"devilmay","price" : 25000 , "description" : "[Click HERE](https://images.wallpapersden.com/image/download/devil-may-cry-5-4k_a2hubWyUmZqaraWkpJRmZ21lrWxnZQ.jpg) for Image Preview" } ,
            {"name":"binary","price" : 100000 , "description" : "[Click HERE](https://wallpaperaccess.com/full/4220753.jpg) for Image Preview" },
            {"name":"naruto","price" : 80000 , "description" : "[Click HERE](https://images.hdqwalls.com/download/kakashi-hatake-anime-4k-yk-1280x720.jpg) for Image Preview" },
            {"name":"pubg","price" : 30000 , "description" : "[Click HERE](https://hdqwalls.com/download/pubg-android-game-4k-eh-1280x720.jpg) for Image Preview" },
            {"name":"blocks","price" : 5000 , "description" : "[Click HERE](https://cdn.wallpapersafari.com/77/30/wKc3Jy.jpg) for Image Preview" }]

collectibles = [{"name":"Coin", "price" : 1500000, "description" : "A very rare coin which is owned by only a few rich members of the server"},
                {"name":"Vinyl Record", "price" : 1000000, "description" : "Go down the memory lane to discover the beginning of the music era"},
                {"name":"Old Stamp", "price" : 500000, "description" : "Collect some of the rarest stamps"},
                {"name":"Slot Machine", "price" : 5000000, "description" : "Purchase a slot machine just to flex over your friends"}]

animals = ["hamster", "rabbit", None, "fox", "bear", "chicken", "mouse", "pig", None, "koala", "wolf", "boar"]
fishes = ["fish", None, "whale", "blowfish", "lobster", None, "octopus", "squid", "dolphin", "shark", "seal"]
dig = ["soccer", "boomerang", None, "badminton", "lacrosse", "dart", "jigsaw", "violin", "trophy", None, "syringe", "pill"]
# collectibles = ["slot_machine", "key", "dolls", "statue_of_liberty"]

names = ["Jenny", "Lauren", "Humble", "Dan", "Matthew", "Blacksmith", "Clarke", "Simon", "Christian", "Hector", "Albert", "Vader", "Paul", "Jeremy"]
beg_names = ["Rick Astley",
              "Shrek",
              "Jesus",
              "Dank Memer",
              "Mr Mosby",
              "Wendy",
              "Barry McKocner",
              "Jordan Peele",
              "Harry Balzac",
              "Kevin Hart",
              "Kim Jong Un",
              "Drake",
              "Kamala Harris",
              "Chris Peanuts",
              "A honey badger",
              "Discord Dog",
              "Rihanna",
              "Mr. Clean",
              "Satan",
              "ayylien",
              "Selena Gomez",
              "Harry",
              "Elizabeth Warren",
              "Dawn Keebals",
              "Billie Eyelash",
              "Joe Montana",
              "Mr. Ja-cough",
              "Your step-sister",
              "Chuck Norris",
              "Your drunk self",
              "Dr. Phil",
              "Default Jonesy",
              "Cardi B",
              "Sans",
              "Peter Dinklage",
              "Nicki Minaj",
              "Dwight Shrute",
              "Timmy",
              "Demi Lovato",
              "Donald Glover",
              "That fart you've been holding in",
              "Paula Deen",
              "Lady Gaga",
              "Oprah",
              "Elon Musk",
              "Taylor Swift",
              "Melmsie's Beard",
              "Justin Bieber",
              "Toby Turner",
              "That girl whose bed you woke up in last night and you're too afraid to ask her name because you might come off as rude",
              "AirPod Jerk",
              "Your mom",
              "Mike Hoochie",
              "Mike Ock",
              "Spoopy Skelo",
              "Chungus",
              "Flo from Progressive",
              "That tiktok star that shows a little too much butt",
              "Sir Cole Jerkin",
              "T series",
              "Jennifer Lopez",
              "Barack Obama",
              "Cersei Lannister",
              "Carole Baskin",
              "Gordon Ramsay",
              "Thanos",
              "Emilia Clarke",
              "B Simpson",
              "Bongo cat",
              "Keanu Reeves",
              "Mr. Beast",
              "Annoying Ass Clown",
              "That lion from the kids movie that vaguely resembles the story of Jesus Christ",
              "That imposter who was too scared to murder you just because he didn't want to look sus",
              "TikTok Moron",
              "Alotta Fagina",
              "Joe",
              "SSSniperWolf",
              "SSundee" ,
              "JoniOliveros",
              "MargeJerman",
              "SteveMarrow",
              "SierraSultan", 
              "PaigeTelecanos", 
              "Messi",
              "Raibaru Fumetsu",
              "Yandere-Chan",
              "Megami Saikou",
              "Umeji Kizugichi",
              "Kokichi Ouma",
              "Jessica Carter",
              "Osoro Shidesu",
              "Hokuto Furukizu",
              "Dairoku Surikuzau",
              "Hayanari Tsumeato",
              "Kuroko Kamenaga",
              "The Gym Teacher",
              "A teacher",
              "Four Students",
              "Gaku Hikitsuri",
              "Shiromi Torayoshi",
              "Oka Ruto",
              "Osana Najimi",
              "Doctor Slone",
              "Brutus",
              "Jules",
              "@YandereDev",
              "Senpai",
              "Gideon Gray",
              "MontoHamacles",
              "AminiDruke",
              "Mida Rana",
              "Midori Gurin",
              "Senpai's Sister",
              "Huggy Wuggy",
              "Pickle Rick",
              "Purple Guy",
              "Jamesbf",
              "James Charles",
              "Dhar Mann",
              "DEVS",
              "Hawka",
              "Slick",
              "BluesNoobs",
              "Memecat"]

neg_response = ["be gone",
                "coin.exe has stopped working",
                "I only give money to my mommy",
                "go ask someone else",
                "Well, let's ask another person",
                "I share money with no-one",
                "the atm is out of order, sorry",
                "bye jerk, no coins for you",
                "ew no",
                "Back in my day we worked for a living",
                "I would not share with the likes of you",
                "honestly why are you even begging, get a job",
                "ew get away",
                "can you not",
                "nah, would rather not feed your gambling addiction",
                "I need my money to buy airpods",
                "ur too stanky",
                "ur not stanky enough",
                "Oh hell/BAD-WORD nah",
                "stop begging",
                "Sure take this nonexistent coin",
                "no coins for you",
                "there. is. no. coins. for. you.",
                "You get nothing",
                "no u",
                "Get a job you hippy",
               " No way, you'll just use it to buy pink phallics",
                "I give people nothing ",
                "get the heck/censored out of here, you demon!",
                "I would sooner spend money on taxes than giving you anything",
                "get lost u simp",
                "get out of here, moron, get clapped on!",
                "I don't share with the n-words",
                "pull urself up by your bootstraps scrub",
                "HeRe In AmErIcA wE dOnT dO cOmMuNiSm",
                "Imagine begging in 2022, gofundme is where it is at",
                "sure take this non-existent coin"]

class Economy(commands.Cog):
    """Economy related commands"""
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.transactions = []
    
    async def add(self, id, amount = 0):
        bal = await self.bot.db.fetchrow("SELECT money FROM economy WHERE userid = $1", id)
        await self.bot.db.execute("UPDATE economy SET money = $1 WHERE userid = $2", amount + bal[0], id)
    
    async def get(self, id):
        user = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userid = $1", id)
        return user
    
    async def check(self, id):
        user = await self.bot.db.fetch("SELECT * FROM economy WHERE userid = $1", id)
        if not user:
            await self.bot.db.execute("INSERT INTO economy (userid, money, inventory, bgs) VALUES ($1, $2, $3, $4)", id, 0, [], ["default"])
    
    async def sub(self,id,name):
        data = await self.bot.db.fetchrow("SELECT inventory FROM economy WHERE userid = $1", id)
        data = list(data[0])
        data.remove(name)
        await self.bot.db.execute("UPDATE users SET inventory = $1 WHERE userid = $2 ", data, id)
    
    async def charts(self):
        tops = await self.bot.db.fetch("SELECT * FROM economy ORDER BY money DESC NULLS LAST")
        top = {}
        for i in tops:
            top[i[0]] = i[1]
        return top
    
    async def add_item(self, id, item):
        inventory = await self.bot.db.fetchrow("SELECT inventory FROM economy WHERE userid = $1", id)
        if inventory:
            inventory = inventory[0]
        else:
            inventory = []
        
        inventory.append(item)
        await self.bot.db.execute("UPDATE economy SET inventory = $1 WHERE userid = $2", inventory, id)
    
    async def invent(self, id):
        inventory = await self.bot.db.fetchrow("SELECT inventory FROM economy WHERE userid = $1", id)
        return inventory[0]

    
    async def available(self, id):
        urls = await self.bot.db.fetchrow("SELECT bgs FROM economy WHERE userid = $1",id)
        return urls[0]

    async def update(self, id, list):
        await self.bot.db.execute("UPDATE economy SET bgs = $1 WHERE userid = $2", list, id)
    

    @commands.command(aliases = ["earn", "typerace"])
    @commands.cooldown(1, 60, type = commands.BucketType.user)
    async def work(self, ctx):
        """Earn money through typeracing :moneybag:"""
        await self.check(ctx.author.id)
        sentence = choice(sentences)
        length = len(sentence.split())
        # formatted = re.sub(r'[^A-Za-z ]+', "", sentence).lower()
        # emoji = ""

        # for i in formatted:
        #     if i == " ":
        #         emoji += "   "
        #     else:
        #         emoji += f":regional_indicator_{i}: "
        await ctx.send("Race against time to complete the following sentence as fast as possible.\n The faster you complete, the more coins you get!")
        
        send = await ctx.send(f"```yml\n{sentence}\n```")

        e = discord.Embed(description = "You failed to answer correctly in time.\n You got `100` :moneybag: for an hour of work", color = ctx.author.color, timestamp = datetime.utcnow())

        try:
            msg = await self.bot.wait_for("message", timeout = 60.0, check = lambda message : message.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send(embed = e)
            await self.add(ctx.author.id, 100)
        else:
            if msg.content.lower() == sentence.lower():
                time = str(datetime.utcnow() - send.created_at)
                time_format = time[:-5][5:]
                if time_format[0] == "0":
                    time_format = time_format[1:]
                
                e = discord.Embed(description = f"{ctx.author.mention} has completed the typerace in **{time_format}** seconds", color = ctx.author.color, timestamp = datetime.utcnow())
                wpm = int(length/(float(time_format)/60))
                money = (wpm/100)*200
                e.add_field(name = "Money Earned :moneybag: - ", value = money)
                e.add_field(name = "WPM - ", value = wpm)
                e.set_thumbnail(url = ctx.author.avatar_url)

                await ctx.send(embed = e)
                await self.add(ctx.author.id, money)
            else:
                await ctx.send(embed = e)
                await self.add(ctx.author.id, 100)
    
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def beg(self, ctx):
        """Beg for earning some coins"""
        await self.check(ctx.author.id)

        money = [0 , 0, 0, random.randint(10, 2000), random.randint(30, 500), 0, random.randint(100, 200), random.randint(1, 2500), random.randint(2, 300)]
        amount = random.choice(money)
        person = random.choice(beg_names)
        response = random.choice(neg_response)
        await self.add(ctx.author.id, amount)

        if amount == 0:
            e = discord.Embed(title = person, description = response, color = discord.Color.red())
            e.set_footer(text = "Imagine Begging LMAO")
            await ctx.send(embed = e)
            return
        else:
            e = discord.Embed(title = person, description = f"Oh poor little beggar, here take these `{amount}` coins", color = discord.Color.random())
            await ctx.send(embed = e)
            return
    
    @commands.command(aliases = ["bal", "money"])
    async def balance(self, ctx, member : discord.Member = None):
        """Shows the balance of the user"""
        if not member:
            member = ctx.author
        
        await self.check(member.id)
        user = await self.get(member.id)
        money = user[1]

        e = discord.Embed(title = ":moneybag: Total Balance", description = f"{member.mention} has a total of `{money}` coins", color = member.color, timestamp = datetime.utcnow())
        e.set_thumbnail(url = member.avatar_url)
        await ctx.send(embed = e)
    
    @commands.command()
    async def give(self, ctx, member : discord.Member, amount : int):
        """Give some coins to another user"""
        await self.check(member.id)
        await self.check(ctx.author.id)
        user = await self.get(ctx.author.id)
        money = user[1]

        if money < amount:
            await ctx.send("You don't have that much coins to give. Go earn some money first.")
        else:        
            await self.add(ctx.author.id, -amount)
            await self.add(member.id, amount)
            await ctx.send(f"**{ctx.author.name}** has given `{amount}` coins to **{member.name}** out of generousity.")
    
    @commands.command()
    async def gamble(self, ctx, amount : int):
        """Gamble money to win 50-100% of the original money"""
        id = ctx.author.id
        await self.check(id)

        if amount < 100:
            return await ctx.send(embed = discord.Embed(description = "You need to bet atleast 100 coins :moneybag: in slots.", color = ctx.author.color, timestamp = datetime.utcnow()))
        
        user = await self.get(id)
        money = user[1]

        if money < amount:
            return await ctx.send(embed = discord.Embed(description = "You don't have the given amount of coins in your account :expressionless:.", color = discord.Color.red(), timestanmp = datetime.utcnow()))
        user_strikes = randint(1, 14)
        bot_strikes = randint(3, 14)

        if user_strikes > bot_strikes:
            percent = randint(50, 100)
            amount_won = int(amount * (percent/100))
            await self.add(id, amount_won)
            user = await self.get(id)

            e = discord.Embed(description = f"""You won **{amount_won}** coins :moneybag:. Percent won : **{percent}%**.\n New Balance : **{user[1]}** coins :money:""", color = ctx.author.color, timestamp = datetime.utcnow())
            e.set_author(name = f"Wow!! Seems like **{ctx.author.name}** plays well!!", icon_url = ctx.author.avatar_url)
        
        elif user_strikes < bot_strikes:
            percent = randint(0, 80)
            amount_lost = int(amount * (percent/100))
            await self.add(id, -amount_lost)
            user = await self.get(id)

            e = discord.Embed(description = f"""You lost **{amount_lost}** coins :moneybag:. Percent lost : **{percent}%**.\n New Balance : **{user[1]}** coins :money:""", color = ctx.author.color, timestamp = datetime.utcnow())
            e.set_author(name = f"Crap play from **{ctx.author.name}**!", icon_url = ctx.author.avatar_url)
        
        else:
            e = discord.Embed(description = f"""**IT IS A TIE!!**""", color = ctx.author.color, timestamp = datetime.utcnow())
            e.set_author(name = f"TIE", icon_url = ctx.author.avatar_url)
        
        e.add_field(name = f"**{ctx.author.name.title()}**", value = f"Strikes `{user_strikes}`")
        e.add_field(name = f"**{self.bot.user.name.title()}**", value = f"Strikes `{bot_strikes}`")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["slot", "bet"])
    async def slots(self, ctx, amount : int):
        """Bet your money in slots for a chance to win 20 times the money or loose it all"""
        id = ctx.author.id
        await self.check(id)

        if amount < 100:
            return await ctx.send(embed = discord.Embed(description = "You need to bet atleast 100 coins :moneybag: in slots.", color = ctx.author.color, timestamp = datetime.utcnow()))
        
        user = await self.get(id)
        money = user[1]

        if money < amount:
            return await ctx.send(embed = discord.Embed(description = "You don't have the given amount of coins in your account :expressionless:.", color = discord.Color.red(), timestanmp = datetime.utcnow()))
        
        outcomes = []
        for i in range(3):
            outcome = choice([":coin:", ":money_mouth:", ":money_with_wings:"])
            outcomes.append(outcome)

        if outcomes[0] == outcomes[1] == outcomes[2]:
            await self.add(id, amount * 20)
            user = await self.get(id)

            e = discord.Embed(title = "   ".join(outcomes), description = f"Congratulations!! {ctx.author.mention} have won {amount}x20 coins :moneybag: using the slots. \n Total Money : {user[1]}", color = ctx.author.color, timestamp = datetime.utcnow())
        else:
            await self.add(id, -amount)
            user = await self.get(id)

            e = discord.Embed(title = "   ".join(outcomes), description = f"Oh No!! {ctx.author.mention} have lost {amount} coins :moneybag: using the slots. \n Total Money : {user[1]}", color = ctx.author.color, timestamp = datetime.utcnow())
        
        e.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["globallb"])
    async def glb(self, ctx):
        """Shows the global charts of economy"""
        tops = await self.charts()
        bg = Image.open("./Assets/images/global_lb.png")
        font = ImageFont.truetype("./Assets/fonts/bahnschrift.ttf", size = 13)
        font_big = ImageFont.truetype("./Assets/fonts/bahnschrift.ttf", size = 25)

        x, x1, y, y_ = 90, 400, 90, 66
        
        draw = ImageDraw.Draw(bg)
        draw.text((5, 727), str(datetime.now().strftime("%d %b, %Y")), fill = (255, 255, 255), font = font)

        counter = 10
        for id, money in tops.items():
            user = self.bot.get_user(id)
            if not user:
                continue
            name = f"user.name.title()[:20].." if len(str(user.name)) > 20 else user.name.title()
            draw.text((x, y), name, fill = (255, 255, 255), font = font_big)
            draw.text((x1, y), str(money), fill = (255, 255, 255), font = font_big)
            
            y += y_
            counter -= 1

            if counter == 0:
                break
        
        while counter > 0:
            draw.text((x, y), "    -    ", fill = (255, 255, 255))
            draw.text((x1, y), "    -    ", fill = (255, 255, 255))

            y += y_
            counter -= 1
        
        with BytesIO() as a:
            bg.save(a, "PNG")
            a.seek(0)
            await ctx.send(file = discord.File(a, filename = "global_leader.png"))
    
    @commands.command(aliases = ["serverlb"])
    async def lb(self, ctx):
        """Shows the server's chart of economy"""
        bg = Image.open("./Assets/images/server_lb.png")
        font = ImageFont.truetype("./Assets/fonts/bahnschrift.ttf", size = 13)
        font_big = ImageFont.truetype("./Assets/fonts/bahnschrift.ttf", size = 25)

        x, x1, y, y_ = 90, 400, 90, 66
        tops = await self.charts()
        datas = {}
        for i in ctx.guild.members:
            money = await self.get(i.id)
            if money is not None:
                datas[i.id] = money[1]
        
        # print(f"before sorting - {datas}")
        newdata = sorted(datas.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
        # print(f"after sorting - {newdata}")

        draw = ImageDraw.Draw(bg)

        counter = 10
        for i in newdata:
            id, money = i[0], i[1]
            user = self.bot.get_user(id)
            name = f"{user.name.title()[:20]}.." if len(str(user.name)) > 20 else user.name.title()
            name = f"{user.name.title()[:20]}.." if len(str(user.name)) > 20 else user.name.title()
            draw.text((x, y), name, fill = (255, 255, 255),font = font_big)
            draw.text((x1, y), str(money), fill = (255, 255, 255), font = font_big)
            y += y_
            counter -= 1
            if counter == 0:
                break
        
        while counter > 0:
            draw.text((x, y), "    -    ", fill=(255, 255, 255))
            draw.text((x1, y), "    -    ", fill=(255, 255, 255))
            y += y_
            counter -= 1
        
        with BytesIO() as a:
            bg.save(a, 'PNG')
            a.seek(0)
            await ctx.send(file = discord.File(a, filename = "server_leader.png"))
    
    @commands.command(aliases = ["hunting"])
    @commands.cooldown(1, 600, type = commands.BucketType.user)
    async def hunt(self, ctx):
        """Hunt down animals and sell them for money"""
        id = ctx.author.id
        await self.check(id)
        animal = choice(animals)
        if animal:
            e = discord.Embed(title = "Hunting Results", description = f"Nice play! You hunted down a {animal.title()} :{animal}:", color = ctx.author.color, timestamp = datetime.utcnow())
            await self.add_item(id, animal)
        else:
            e = discord.Embed(title = "Hunting Results", description = "AHH! You found nothing. Better do a bit of practice before your next hunt :confused:", color = ctx.author.color, timestamp = datetime.utcnow())
        
        e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        e.set_footer(text = f"Type `inventory` to check your inventory.")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["fishing"])
    @commands.cooldown(1, 300, type = commands.BucketType.user)
    async def fish(self, ctx):
        """Catch fishes and sell them for money"""
        id = ctx.author.id
        await self.check(id)
        fish = choice(fishes)
        if fish:
            e = discord.Embed(title = "Fishing Results", description = f"Nice play! You captured a {fish.title()} :{fish}:", color = ctx.author.color, timestamp = datetime.utcnow())
            await self.add_item(id, fish)
        else:
            e = discord.Embed(title = "Fishing Results", description = "AHH! You found nothing. Better have more patience. :confused:", color = ctx.author.color, timestamp = datetime.utcnow())
        
        e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        e.set_footer(text = f"Type `inventory` to check your inventory.")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["digging"])
    @commands.cooldown(1, 900, type = commands.BucketType.user)
    async def dig(self, ctx):
        """Dig to explore hidden items and sell them for money"""
        id = ctx.author.id
        await self.check(id)
        item = choice(dig)
        if item:
            e = discord.Embed(title = "Digging Results", description = f"Voila! You found a {item.title()} :{item}:", color = ctx.author.color, timestamp = datetime.utcnow())
            await self.add_item(id, item)
        else:
            e = discord.Embed(title = "Digging Results", description = "AHH! You found nothing. Better luck next time. :confused:", color = ctx.author.color, timestamp = datetime.utcnow())
        
        e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        e.set_footer(text = f"Type `inventory` to check your inventory.")
        await ctx.send(embed = e)
    
    @commands.command(aliases = ["inventory"])
    async def inv(self, ctx, member : discord.Member = None):
        """See what is available in your or others inventory"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        member = member or ctx.author
        await self.check(member.id)

        user = await self.get(member.id)
        inv = user[2]

        fishes_ = [f"**{inv.count(i)}** x {i} :{i}:" for i in fishes if i in inv]
        animals_ = [f"**{inv.count(i)}** x {i} :{i}:" for i in animals if i in inv]
        dig_ = [f"**{inv.count(i)}** x {i} :{i}:" for i in dig if i in inv]
        collectibles_ = [f"**{inv.count(i)}** x {i}" for i in collectibles if i in inv]
        
        fishes_ = "\n".join(fishes_) if len(fishes_) >= 1 else "*No fishes in Inventory*"
        animals_ = "\n".join(animals_) if len(animals_) >= 1 else "*No animals in Inventory*"
        dig_ = "\n".join(dig_) if len(dig_) >= 1 else "*No items in Inventory*"
        collectibles_ = "\n".join(collectibles_) if len(collectibles_) >= 1 else "*No collectibles in Inventory*"
        
        e = discord.Embed(title = "Inventory", description = f"Type `{prefix}sell <item_name>` to sell non-collectible items", color = ctx.author.color, timestamp = datetime.utcnow())
        e.add_field(name = "Animals", value = animals_)
        e.add_field(name = "Fishes", value = fishes_)
        e.add_field(name = "Items", value = dig_)
        e.add_field(name = "Collectibles", value = collectibles_)
        e.set_thumbnail(url = "https://cdn-icons-png.flaticon.com/512/831/831840.png")

        await ctx.send(embed = e)
    
    @commands.command()
    async def sell(self, ctx, item = "all"):
        """Sell your non-collectible items for money"""
        id = ctx.author.id
        await self.check(id)
        data = await self.get(id)
        
        inventory = data[2]

        if id in self.transactions:
            return await ctx.send("You already have one transaction going on with another person, Please cancel the transaction to start a new one.")
        
        self.transactions.append(id)

        def cost(product):
            if product in dig:
                return randint(900, 1200)
            elif product in animals:
                return randint(700, 1000)
            elif product in fishes:
                return randint(500, 800)

        sellables = [i for i in inventory if i not in collectibles]
        name = choice(names)
        item = item.lower()

        total_amount = 0
        total_count = 0

        if item == "all":
            if len(sellables) == 0:
                await self.transactions.remove(id)
                return await ctx.send("You don't have any sellable item in your inventory :expressionless:", delete_after = 5)
            total_count = len(sellables)
            for i in sellables:
                total_amount += cost(i)
            
            e = discord.Embed(title = "Offer", description = f"{name} is offering you {total_amount} coins for all of your item(s) (**{total_count}**)", color = discord.Color.random(), timestamp = datetime.utcnow())
        
        elif item in sellables:
            total_count = sellables.count(item)
            total_amount = total_count * cost(item)

            e = discord.Embed(title = "Offer", description = f"{name} is offering you {total_amount} coins for **{total_count} x {item}** :{item}:", color = discord.Color.random(), timestamp = datetime.utcnow())
        
        else:
            await self.transactions.remove(id)
            return await ctx.send("No such sellable item in your inventory :expressionless:", delete_after = 5)
        
        e.set_footer(text = "Rates of items keeps on fluctuating, you can decline the offer and try again later.")
        e.set_author(name = f"For {ctx.author.name}", icon_url = ctx.author.avatar_url)
        e.set_thumbnail(url = "https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhoutte.png")
        msg = await ctx.send(embed = e)

        await msg.add_reaction("✅")
        await msg.add_reaction("❎")

        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ["✅", "❎"]
        
        try:
            reaction = await self.bot.wait_for("reaction_add", timeout = 20.0, check = check)
        except asyncio.TimeoutError:
            e.title, e.description, e.color = "Offer Declined", f"{ctx.author.name} didn't react on time", discord.Color.red()
            await msg.edit(embed = e)
        else:
            if reaction[0].emoji == "✅":
                e.title, e.description, e.color = "Offer Accepted!", f"You sold the item(s) for `{total_amount}` coins", discord.Color.green()
                await self.add(id, total_amount)
                if item == "all":
                    for i in sellables:
                        inventory.remove(i)
                else:
                    while item in inventory:
                        inventory.remove(item)

                await self.bot.db.execute("UPDATE economy SET inventory = $1 WHERE userid = $2", inventory, id)
                await msg.edit(embed = e)
            else:
                e.title, e.description, e.color = "Offer Declined!", "You declined the offer", discord.Color.red()
                await msg.edit(embed = e)
        
        self.transactions.remove(id)
    
    @commands.command(aliases = ["market"])
    async def shop(self, ctx):
        """Check the shop for available items up for sale"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]

        e = discord.Embed(title = "Shop", description = f"Type `{prefix}buy <item_name>` to buy an item", color = discord.Color.random())
        
        for item in shopping:
            name = item["name"].title()
            price = item["price"]
            description = item["description"]
            e.add_field(name = name, value = f"Price : `{price}`\n Description : {description}")
        
        e.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
        await ctx.send(embed = e)
    
    @commands.command()
    async def pawnshop(self, ctx):
        """A shop for unique and antique items"""
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]

        e = discord.Embed(title = "Pawn Shop", description = f"Type `{prefix}collect <item_name>` to add the item to your inventory", color = discord.Color.random())

        for col in collectibles:
            name = col["name"].title()
            price = col["price"]
            description = col["description"]
            e.add_field(name = name, value = f"Price : `{price}`\n Description : {description}")
        
        e.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
        await ctx.send(embed = e)
    
    @commands.command()
    async def buy(self, ctx, *, item):
        """Buy items available in the shop"""
        item = item.lower()
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        await self.check(ctx.author.id)
        balance = await self.get(ctx.author.id)
        balance = balance[1]
        backs = await self.available(ctx.author.id)

        for back in shopping:
            if item == back["name"]:
                if balance > back["price"]:
                    if item not in backs:
                        e = discord.Embed(title = "Purchase Successful!", description = f"{ctx.author.mention} have successfully bought the {item.title()} background image.", color = discord.Color.random(), timestamp = datetime.utcnow())
                        e.set_thumbnail(url = ctx.author.avatar_url)
                        e.set_footer(text = f"You can check your profile by typing `{prefix}profile`")
                        await self.add(ctx.author.id, -1 * back["price"])
                        await ctx.send(embed = e)
                        backs.insert(0, item)
                        await self.update(ctx.author.id, backs)
                        return
                    else:
                        e = discord.Embed(title = "Purchase Failed!", description = f"{ctx.author.mention} already have the {item.title()} background image", color = discord.Color.random(), timestamp = datetime.utcnow())
                        await ctx.send(embed = e, delete_after = 8)
                        return
                else:
                    e = discord.Embed(title = "Failed!", description = f"You don't have sufficient coins to buy {item.title()} background image", color = discord.Color.random(), timestamp = datetime.utcnow())
                    await ctx.send(embed = e, delete_after = 8)
                    return
            else:
                pass
        
        await ctx.send(embed = discord.Embed(title = "No Items Available", description = f"There is no such items in the shop, please recheck the name of the item before buying", color = discord.Color.random(), timestamp = datetime.utcnow()))
    
    @commands.command()
    async def collect(self, ctx, *, item):
        """Be the richest member in your server and add some unique and antique items to your collection"""
        item = item.lower()
        prefix = await self.bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", ctx.guild.id)
        prefix = prefix[0]
        await self.check(ctx.author.id)
        balance = await self.get(ctx.author.id)
        balance = balance[1]

        for collect in collectibles:
            if item == collect["name"]:
                if balance > collect["price"]:
                    e = discord.Embed(title = "Purchase Successful!", description = f"{ctx.author.mention} have successfully purchased {item.title()}.\n It has been added to your inventory (Type {prefix}inv to find your item)", color = discord.Color.random(), timestamp = datetime.utcnow())
                    e.set_thumbnail(url = ctx.author.avatar_url)
                    await self.add(ctx.author.id, -1 * collect["price"])
                    await self.add_item(ctx.author.id, item)
                    await ctx.send(embed = e)
                    return
                else:
                    e = discord.Embed(title = "Failed!", description = f"You don't have sufficient coins to buy {item.title()}", color = discord.Color.random(), timestamp = datetime.utcnow())
                    await ctx.send(embed = e, delete_after = 8)
                    return
            else:
                pass
        
        await ctx.send(embed = discord.Embed(title = "No Items Available", description = f"There is no such items in the shop, please recheck the name of the item before buying", color = discord.Color.random(), timestamp = datetime.utcnow()))
            


def setup(bot):
    bot.add_cog(Economy(bot))