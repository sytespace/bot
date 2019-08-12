import discord
import random
import asyncio
from discord.ext import commands
from itertools import cycle
from urllib.parse import urlparse
import psycopg2
import datetime
import pyping
import pyspeedtest
import secrets
import json



# Variables

logChannel = 610156083259899904
adminRoles = ["605456866775924746", "566249728732561410"]
TOKEN = open("TOKEN.TXT", "r").read()
url = "postgre db url"

# Define Bot

bot = commands.Bot(command_prefix = 'd!')

# Databases

result = urlparse(url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
db = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users(
                      UserID BIGSERIAL,
                      Xp INTEGER,
                      Tokens INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS Ecopp(
                      UserID BIGSERIAL,
                      Boost BOOLEAN)""")

c.execute("""CREATE TABLE IF NOT EXISTS Activity(
                      UserID BIGSERIAL,
                      GlobalMessages INTEGER,
                      GlobalRank INTEGER,
                      WeeklyMessages INTEGER,
                      WeeklyRank INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS Tickets(
                      Number INTEGER)""")



@bot.event
async def on_ready():
    print("--------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    return

bot.remove_command('help')

# Events

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='announcements')
    await channel.send(f'Welcome {member.display_name} To {member.guild.name} Have A Great Time ...')
    
    with open('./json/users.json', 'r') as c:
        usersJson = c

    if not member.id in usersJson:
        username = str(member.display_name) # get display name
        userJson[str(member.id)] = {}
        usersJson[str(member.id)]['username'] = username # use username variable deffined above
        usersJson[str(member.id)]['bal'] = 0 # default ballence
        usersJson[str(member.id)]['admin'] = 0 # 0 is Normal / <1 is an admin

    with open('./json/users.json', 'w') as c:
        json.dump(usersJson, c) # dump data

@bot.event
async def on_message(message):
	with open('./json/users.json', 'r') as c:
		usersJson = c 
	randomInt = random.randint(5,25) # Get Random Number
	usersJson[str(member.id)]['bal'] = randomInt
	with open('./json/users.json', 'w') as c:
        json.dump(usersJson, c) # dump data

	await bot.process_commands(message) # Run Command 

# Commands

bot.command()
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    create_economypp(member.id)
    checklevelup(member.id)
    xp = get_xp(member.id)
    tk = get_tk(member.id)
    lvl = get_lvl(member.id)
    booster = getbooster(member.id)
    #if tk <= 0:
        #set_xp(ctx.message.author.id, 0)
        #print("SET VALUE TO 0")
    if tk <= 0:
        set_tk(ctx.message.author.id, 0)
        print("SET VALUE TO 0")
    embed = discord.Embed(color=0x363942)
    embed.add_field(name="XP", value=f"{xp}", inline=False)
    embed.add_field(name="Sytes", value=f"${tk}", inline=False)
    embed.add_field(name="Level", value=f"{lvl}", inline=False)
    embed.add_field(name="Booster", value=f"{booster}", inline=False)
    embed.add_field(name="Joined server at", value=member.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_author(name=f"{member.display_name}'s profile.")
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.say(embed=embed)

# bot.command()
# async def cat(ctx):

# bot.command()
# async def dog(ctx):

# bot.command()
# async def serverinfo(ctx):

# bot.command()
# async def weekly_reset(ctx):

@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    embed = discord.Embed(color=0xA121FF)
    embed.add_field(name="Our bot's uptime :calendar_spiral:", value=f"Weeks: **{weeks}**\nDays: **{days}**\nHours: **{hours}**\nMinutes: **{minutes}**\nSeconds: **{seconds}**")
    await ctx.send(embed=embed)

# bot.command()
# async def pfp(ctx):

# bot.command()
# async def purge(ctx, number):

# bot.command()
# async def checkuser(ctx):

# bot.command()
# async def genpw(ctx):

# bot.command()
# async def shop(ctx):

# bot.command()
# async def buy(ctx):
    
bot.command()
async def ban(ctx, member: discord.Member = None, *, reason="Sorry You Have Been Banned"):
    if ctx.author.roles in adminRoles:
        if member == None: # No Member Specified
            await ctx.send("Please Specify A Member")
            await ctx.message.delete() # Delete The Message
        else:
            dm = discord.Embed(title = "You have been banned from `SyteSpace`!", description = "Details about the ban:", color =0x363942)
            dm.add_field(name = ":closed_lock_with_key: Moderator:", value = ctx.message.author.display_name)
            dm.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
            dm.set_thumbnail(url=member.avatar_url)
            logEmb = discord.Embed(title = "Ban Issued!", description = "Details about the ban:", color =0x363942)
            logEmb.add_field(name = "Moderator:", value = f"{ctx.message.author.display_name}")
            logEmb.add_field(name = ":spy: member Banned:", value = f"{member.name}")
            logEmb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
            logEmb.set_thumbnail(url=member.avatar_url)
            log = bot.get_channel(logChannel)
            await member.send(embed=dm) # Send DM
            await member.ban(reason=reason) # Ban
            await log.send(embed=logEmb) # Send To Log
            await ctx.message.delete() # Delete The Message
    else:
        await ctx.send("You Dont Have Permition To Run This Command ...") # Message in CTX Channel
        await ctx.message.delete() # Delete The Message
        

bot.command()
async def kick(ctx, member: discord.Member = None, *, reason="Sorry You Have Been Kicked"):
    if ctx.author.roles in adminRoles:
        if member == None: # No Member Specified
            await ctx.send("Please Specify A Member")
            await ctx.message.delete() # Delete The Message
        else:
            dm = discord.Embed(color =0x363942, title="You have been kicked from `SyteSpace`!")
            dm.set_thumbnail(url=member.avatar_url)
            dm.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
            dm.add_field(name="Moderator:", value=ctx.message.author.display_name)
            logEmb = discord.Embed(color =0x363942, title="A kick has been issued")
            logEmb.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
            logEmb.add_field(name="Moderator:", value=ctx.message.author.display_name)
            logEmb.add_field(name=":spy: User Kicked:", value=f"{member.name}")
            logEmb.set_thumbnail(url=member.avatar_url)
            log = bot.get_channel(logChannel)
            await member.send(embed=dm) # Send DM
            await member.kick(reason=reason) # Kick
            await log.send(embed=logEmb) # Send To Log
            await ctx.message.delete() # Delete The Message
    else:
        await ctx.send("You Dont Have Permition To Run This Command ...") # Message in CTX Channel
        await ctx.message.delete() # Delete The Message
        
# bot.command()
# async def unban(ctx):

# bot.command()
# async def mute(ctx):

    
@bot.command()
async def help(ctx): #bot stop giving errors s
    embed = discord.Embed(title = "What Information Do You Require?", description = "React with 💬 for a list of user commands, 💰 for a list of economy commands and 🛑 for a list of moderation commands", color=0x363942)
    startmsg = await ctx.send(ctx.message.channel, embed=embed)
    #🏠
    await ctx.message.add_reaction(startmsg, '💬')
    await ctx.message.add_reaction(startmsg, '💰')
    await ctx.message.add_reaction(startmsg, '🛑')
    while True:
        choice = await ctx.wait_for(['💬', '💰', '🛑', '🏠', '❌'])
        if choice.user == bot.user:
            pass
        else:
            if choice.reaction.emoji == '🏠':
                await ctx.remove_reaction(startmsg, '🏠', ctx.message.author)
                await ctx.remove_reaction(startmsg, '🏠', bot.user)
                embed = discord.Embed(title = "What Information Do You Require?", description = "React with 💬 for a list of user commands, 💰 for a list of economy commands and 🛑 for a list of moderation commands", color=0x363942)
                await ctx.edit(startmsg, embed=embed)
                await ctx.message.add_reaction(startmsg, '❌')
            if choice.reaction.emoji == '💬':
                await ctx.remove_reaction(startmsg, '💬', choice.user)
                await ctx.add_reaction(startmsg, '🏠')
                await ctx.add_reaction(startmsg, '❌')
                with open("textfiles/usercmds.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu", description="`[] = Not Required Argument`, `<> = Required Argument`",color=0x363942)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(text=f"Request by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    await ctx.edit(startmsg, embed=embed)
                    await ctx.add_reaction(startmsg, '❌')
                    txtfile.close()
            if choice.reaction.emoji == '💰':
                await ctx.remove_reaction(startmsg, '💰', choice.user)
                await ctx.add_reaction(startmsg, '🏠')
                with open("textfiles/economy.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu", description="`[] = Not Required Argument`, `<> = Required Argument`",color=0x363942)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(text=f"Request by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    await ctx.edit(startmsg, embed=embed)
                    await ctx.add_reaction(startmsg, '❌')
                    txtfile.close()
            if choice.reaction.emoji == '🛑':
                await ctx.remove_reaction(startmsg, '🛑', choice.user)
                await ctx.add_reaction(startmsg, '🏠')
                with open("textfiles/moderation.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu", description="`[] = Not Required Argument`, `<> = Required Argument`",color=0x363942)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(text=f"Request by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    await ctx.edit(startmsg, embed=embed)
                    await ctx.add_reaction(startmsg, '❌')
                    txtfile.close()
            if choice.reaction.emoji == '❌':
                await ctx.remove_reaction(startmsg, '❌', choice.user)
                await ctx.delete(ctx.message)
                await ctx.delete(startmsg)

@bot.command()
async def weekly_reset(ctx):
    if [role.id for role in ctx.message.author.roles] in adminRoles:
        for x in ctx.members:
            uid = x.id
            reset_weeklymessages(uid)
            print(f"[Activity] Reset weekly for {uid}")
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))
                
@bot.command()
async def ping(ctx):
        st = pyspeedtest.SpeedTest()
        google_req = pyping.ping('8.8.8.8')
        cloudflare_req = pyping.ping('1.1.1.1')  
        discord_req = pyping.ping('gateway.discord.gg')
        google = str(google_req.avg_rtt)
        cloudflare = str(cloudflare_req.avg_rtt)
        discord_ping = str(discord_req.avg_rtt)
        ping = str(int(round(st.ping(), 0)))
        down = round((st.download()/1000000), 2)
        up = round((st.upload()/1000000), 2)
        host = str(st.host)
        now = datetime.utcnow()
        old_message = now - ctx.message.timestamp
        old_delta = old_message.microseconds
        milsec_old = int(old_delta // 1000)
        bot_ping = round(bot.latency * 1000 / 2)
        embed = discord.Embed(title="Connection Statistics", description="Current Connection Statistics", color=0x363942)
        embed.add_field(name="Ping (st)", value="`%sms`" % ping, inline=False)
        embed.add_field(name="Ping (heartbeat)", value="`%sms`" % bot_ping, inline=False)
        embed.add_field(name="Server Used", value="`%s`" % host, inline=False)
        embed.add_field(name="Download", value="`%s mbps`" % down, inline=False)
        embed.add_field(name="Upload", value="`%s mbps`" % up, inline=False)
        embed.add_field(name="Google", value="`%sms`" % google, inline=False)
        embed.add_field(name="Cloudflare", value="`%sms`" % cloudflare, inline=False)
        embed.set_footer(text=f"Requested by: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.say(embed=embed)

#Functions

def checklevelup(uid: str):
    currentlvl = get_lvl(uid)
    currentxp = get_xp(uid)
    if currentxp >= 10000:
        if currentlvl != 10:
            set_lvl(uid, 10)
        else:
            pass
    if currentxp >= 20000:
        if currentlvl !=20:
            set_lvl(uid, 10)
        else:
            pass

def create_user_if_not_exists(user_id: str):
    c.execute("SELECT COUNT(*) FROM Users WHERE UserID=%s", (str(user_id),))
    user_count = c.fetchone()[0]
    if user_count < 1:
        print("[Users Table]Creating user with id " + str(user_id))
        c.execute("INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)", (str(user_id), 0, 0, 0, 0, 0))
        db.commit()

def create_economypp(user_id: str):
    c.execute("SELECT COUNT(*) FROM Ecopp WHERE UserID=%s", (str(user_id),))
    verif = c.fetchone()[0]
    if verif < 1:
        print("[Economy++] Creating user with id " + str(user_id))
        c.execute("INSERT INTO Ecopp VALUES (%s, %s)", (str(user_id), False))
        db.commit()

def create_activity(user_id: str):
    c.execute("SELECT COUNT(*) FROM Activity WHERE UserID=%s", (str(user_id),))
    verif = c.fetchone()[0]
    if verif < 1:
        print("[Activity] Creating user with id " + str(user_id))
        c.execute("INSERT INTO Activity VALUES (%s, %s, %s, %s, %s)", (str(user_id), 0, 0, 0, 0))
        db.commit()

def set_lvl(user_id, amount: int):
    lvl = amount
    c.execute("UPDATE Users SET Level=%s WHERE UserID=%s", (lvl, str(user_id)))
    db.commit()
    return lvl

def get_lvl(user_id: str):
    create_user_if_not_exists(user_id)
    create_economypp(user_id)
    c.execute("SELECT Level FROM Users WHERE UserID=%s", (str(user_id),))
    user_lvl = int(c.fetchone()[0])
    db.commit()
    return user_lvl

def setbooster(user_id: str, setto = bool):
    c.execute("UPDATE Ecopp SET Boost=%s WHERE UserID=%s", (bool(setto), str(user_id)))
    db.commit()

def getbooster(user_id: str):
    c.execute("SELECT Boost FROM Ecopp WHERE UserID=%s", (str(user_id),))
    booster = bool(c.fetchone()[0])
    db.commit()
    return booster

def get_xp(user_id: str):
    create_user_if_not_exists(user_id)
    create_economypp(user_id)
    c.execute("SELECT Xp FROM Users WHERE UserID=%s", (str(user_id),))
    user_xp = int(c.fetchone()[0])
    db.commit()
    return user_xp


def add_xp(user_id, amount: int):
    xp = int(get_xp(user_id) + amount)
    c.execute("UPDATE Users SET Xp=%s WHERE UserID=%s", (xp, str(user_id)))
    db.commit()
    return xp

def remove_xp(user_id, amount: int):
    xp = int(get_xp(user_id) - amount)
    c.execute("UPDATE Users SET Xp=%s WHERE UserID=%s", (xp, str(user_id)))
    db.commit()
    return xp

def get_tk(user_id: str):
    create_user_if_not_exists(user_id)
    create_economypp(user_id)
    c.execute("SELECT Tokens FROM Users WHERE UserID=%s", (str(user_id),))
    user_tk = int(c.fetchone()[0])
    db.commit()
    return user_tk


def add_tk(user_id, amount: int):
    tk = int(get_tk(user_id) + amount)
    create_economypp(user_id)
    c.execute("UPDATE Users SET Tokens=%s WHERE UserID=%s", (tk, str(user_id)))
    db.commit()
    return tk

def remove_tk(user_id, amount: int):
    tk = int(get_tk(user_id) - amount)
    c.execute("UPDATE Users SET Tokens=%s WHERE UserID=%s", (tk, str(user_id)))
    db.commit()
    return tk

def set_tk(user_id, amount: int):
    tk = amount
    c.execute("UPDATE Users SET Tokens=%s WHERE UserID=%s", (tk, str(user_id)))
    db.commit()
    return tk

def get_globalmessages(user_id: str):
    create_activity(user_id)
    c.execute("SELECT GlobalMessages FROM Activity WHERE UserID=%s", (str(user_id),))
    user_globalmessages = int(c.fetchone()[0])
    db.commit()
    return user_globalmessages

def get_weeklymessages(user_id: str):
    create_activity(user_id)
    c.execute("SELECT WeeklyMessages FROM Activity WHERE UserID=%s", (str(user_id),))
    user_weeklymessages = int(c.fetchone()[0])
    db.commit()
    return user_weeklymessages

def reset_weeklymessages(user_id: str):
    create_activity(user_id)
    c.execute("UPDATE Activity SET WeeklyMessages=%s WHERE UserID=%s", (0, str(user_id)))
    db.commit()
    return True

def set_weekly_rank(user_id, rank: int):
    c.execute("UPDATE Activity SET WeeklyRank=%s WHERE UserID=%s", (rank, str(user_id)))
    db.commit()
    return rank

def get_user_rank(input_rank: int):
    c.execute("SELECT UserID FROM Activity WHERE WeeklyRank=%s", (int(input_rank),))
    rank = int(c.fetchone()[0])
    db.commit()
    return rank

def add_messages(user_id: str):
    create_activity(user_id)
    globalmsg = int(get_globalmessages(user_id) + 1)
    weeklymsg = int(get_weeklymessages(user_id) + 1)
    c.execute("UPDATE Activity SET GlobalMessages=%s WHERE UserID=%s", (int(globalmsg), str(user_id)))
    c.execute("UPDATE Activity SET WeeklyMessages=%s WHERE UserID=%s", (int(weeklymsg), str(user_id)))
    db.commit()
    return globalmsg + weeklymsg

def isrisk(creation_date):
    inputacc = datetime.utcnow() - creation_date
    accagedays = int(inputacc.days)
    if accagedays <= 7:
        return True
    else:
        return False

# Background Tasks
bot.run(TOKEN)
