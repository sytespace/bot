import discord
import random
import asyncio
import requests
from discord.ext import commands
from discord.utils import get
from urllib.parse import urlparse
import psycopg2
from itertools import cycle
from datetime import datetime, timedelta
import pyping
import pyspeedtest
import secrets
import re

# Define Bot

bot = commands.Bot(command_prefix='s!')
# bot.launch_time = datetime.now()
ongoingpurge = False


@bot.event
async def on_ready():
    print("--------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    return

bot.remove_command('help')  # Removes help, it's as simple as that.

# Variables

logChannel = 573607051297685551
welcomeChannel = 565201713951145994
embcolor = 0x363942
TOKEN = open("TOKEN.TXT", "r").read() # Where is the token? Oh well...
url = open("DATABASE.TXT", "r").read()  # Where is the DB url? Oh well...
spams = {} # Its a dict you idiots...
urlregex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
blockedurls = {}


# Databases

result = urlparse(url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
db = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users(
                      UserID BIGSERIAL,
                      Xp INTEGER,
                      Tokens INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS Ecopp(
                      UserID BIGSERIAL,
                      Boost BOOLEAN)""")

c.execute("""CREATE TABLE IF NOT EXISTS Tickets(
                      Number INTEGER)""")


# Commands
@bot.command()
async def tos(ctx):
    await ctx.send('You can find our ToS at https://github.com/sytespace/Legal')

@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    create_economypp(member.id)
    checklevelup(member.id)
    tk = get_tk(member.id)
    booster = getbooster(member.id)
    #if tk <= 0:
    #set_xp(ctx.message.author.id, 0)
    #print("SET VALUE TO 0")
    if tk <= 0:
        set_tk(ctx.message.author.id, 0)
        print("SET VALUE TO 0")
    embed = discord.Embed(color=embcolor)
    embed.add_field(name="Sytes", value=f"${tk}", inline=False)
    embed.add_field(name="Booster", value=f"{booster}", inline=False)
    embed.add_field(name="Joined server at", value=member.joined_at.__format__(
        '%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_author(name=f"{member.display_name}'s profile.")
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
    response = requests.get('https://aws.random.cat/meow')
    data = response.json()
    embed = discord.Embed(color=embcolor)
    embed.set_image(url=f"{data['file']}")
    react = await ctx.send(embed=embed)
    await react.add_reaction('🐱')
    while True:
        emojis = ['🐱']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == react.id and user.bot is not True:
            if str(reaction.emoji) in emojis:
                await reaction.message.remove_reaction('🐱', user)
                await react.add_reaction('🐱')
                response = requests.get('https://aws.random.cat/meow')
                data = response.json()
                embed = discord.Embed(color=embcolor)
                embed.set_image(url=f"{data['file']}")
                await react.edit(embed=embed)

@bot.command()
async def dog(ctx):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    embed = discord.Embed(color=embcolor)
    embed.set_image(url=f"{data['message']}")
    react = await ctx.send(embed=embed)
    await react.add_reaction('🐶')
    while True:
        dogemojis = ['🐶']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == react.id and user.bot is not True:
            if str(reaction.emoji) in dogemojis:
                await reaction.message.remove_reaction('🐶', user)
                await react.add_reaction('🐶')
                response = requests.get('https://dog.ceo/api/breeds/image/random')
                data = response.json()
                embed = discord.Embed(color=embcolor)
                embed.set_image(url=f"{data['message']}")
                await react.edit(embed=embed)

@bot.command()
async def duck(ctx):
    response = requests.get('https://random-d.uk/api/quack')
    data = response.json()
    embed = discord.Embed(color=embcolor)
    embed.set_image(url=f"{data['url']}")
    react = await ctx.send(embed=embed)
    await react.add_reaction('🦆')
    while True:
        duckemojis = ['🦆']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == react.id and user.bot is not True:
            if str(reaction.emoji) in duckemojis:
                await reaction.message.remove_reaction('🦆', user)
                await react.add_reaction('🦆')
                response = requests.get('https://random-d.uk/api/quack')
                data = response.json()
                embed = discord.Embed(color=embcolor)
                embed.set_image(url=f"{data['url']}")
                await react.edit(embed=embed)

@bot.command()
async def shibe(ctx):
    response = requests.get('http://shibe.online/api/shibes')
    link = response.json()[0]
    embed = discord.Embed(color=embcolor)
    embed.set_image(url=link)
    react = await ctx.send(embed=embed)
    await react.add_reaction('🐕')
    while True:
        duckemojis = ['🐕']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == react.id and user.bot is not True:
            if str(reaction.emoji) in duckemojis:
                await reaction.message.remove_reaction('🐕', user)
                await react.add_reaction('🐕')
                response = requests.get('http://shibe.online/api/shibes')
                link = response.json()[0]
                embed = discord.Embed(color=embcolor)
                embed.set_image(url=link)
                await react.edit(embed=embed)

@bot.command()
async def bird(ctx):
    response = requests.get('https://shibe.online/api/birds')
    link = response.json()[0]
    embed = discord.Embed(color=embcolor)
    embed.set_image(url=link)
    react = await ctx.send(embed=embed)
    await react.add_reaction('🐦')
    while True:
        duckemojis = ['🐦']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == react.id and user.bot is not True:
            if str(reaction.emoji) in duckemojis:
                await reaction.message.remove_reaction('🐦', user)
                await react.add_reaction('🐦')
                response = requests.get('https://shibe.online/api/birds')
                link = response.json()[0]
                embed = discord.Embed(color=embcolor)
                embed.set_image(url=link)
                await react.edit(embed=embed)


@bot.command()
async def new(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.message.author
    server = ctx.message.guild
    numb = get_ticknumb()
    update_ticknumb()
    createchannel = await server.create_text_channel(f"ticket-{numb}")
    embed = discord.Embed(title = f"New ticket created", description = f"Hello {member.display_name}, thanks for reaching out to our support team, a member of staff will be with you as soon as possible.", color=embcolor)
    embed.set_footer(text=f"Ticket number: {createchannel.id}", icon_url=member.avatar_url)
    staff = discord.utils.get(ctx.message.author.guild.roles, name="🔨 Staff")
    guest = discord.utils.get(ctx.message.author.guild.roles, name="👤 Guest")
    client = discord.utils.get(ctx.message.author.guild.roles, name="❤ Client")
    everyone = ctx.message.author.guild.default_role
    disallow = discord.PermissionOverwrite()
    disallow.read_messages = False
    disallow.send_messages = False
    allow = discord.PermissionOverwrite()
    allow.read_messages = True
    allow.send_messages = True
    await createchannel.set_permissions(guest, overwrite=disallow)
    await createchannel.set_permissions(everyone, overwrite=disallow)
    await createchannel.set_permissions(client, overwrite=disallow)
    await createchannel.set_permissions(ctx.message.author, overwrite=allow)
    await createchannel.set_permissions(staff, overwrite=allow)
    await createchannel.send(embed=embed)

@bot.command(pass_context=True)
async def close(ctx):
    channel = ctx.message.channel
    # numb = get_ticknumb()
    embed = discord.Embed(title = "Closing ticket", description = "This ticket will be closed in 60 seconds", color=embcolor)
    confirmmsg = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await channel.delete(reason = "Ticket closed")
        

@bot.command()
async def serverinfo(ctx):
    server = ctx.message.guild
    owner = server.owner
    ownername = owner.display_name
    embed = discord.Embed(
        title=f"Information On {server.name}", description="", color=embcolor)
    embed.add_field(name="Server ID:", value=f"{server.id}", inline=False)
    embed.add_field(name="Server Members:", value=f"{server.member_count}")
    embed.add_field(name="Owner:", value=f"{ownername}", inline=False)
    embed.add_field(name="Region:", value=f"{server.region}", inline=False)
    embed.add_field(name="Verification Level:",
                    value=f"{server.verification_level}", inline=False)
    embed.add_field(name="Server Created At:",
                    value=f"{server.created_at}", inline=False)
    #embed.add_field(name="", value="", inline=False)
    embed.set_thumbnail(url=server.icon_url)
    await ctx.send(embed=embed)


# @bot.command()
# async def uptime(ctx):
#     delta_uptime = datetime.utcnow() - bot.launch_time
#     hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
#     minutes, seconds = divmod(remainder, 60)
#     days, hours = divmod(hours, 24)
#     weeks, days = divmod(days, 7)
#     embed = discord.Embed(color=embcolor)
#     embed.add_field(name="Our bot's uptime :calendar_spiral:",
#                     value=f"Weeks: **{weeks}**\nDays: **{days}**\nHours: **{hours}**\nMinutes: **{minutes}**\nSeconds: **{seconds}**")
#     await ctx.send(embed=embed)

@bot.command()
@commands.has_role(561266182578110474)
async def reset_tickets(ctx):
    var = setup_ticknumb()
    await ctx.send(f"✅ Moderation action completed ({var})")



@bot.command()
@commands.has_role(561266182578110474)
async def statmod(ctx, member: discord.Member = None, amount: int = None):
    # ✅
    if member == None:
        await ctx.send(":x: Please specify a member")
    if amount == None:
        await ctx.send(":x: Please specify an amount")
    else:
        embed = discord.Embed(title=f"What aspect of {member.display_name}'s stats do you wish to change?'", description="React with 📕 to change XP and 📙 to change Sytes and 📗 to toggle booster", color=embcolor)
        wchange = await ctx.send(embed=embed)
        await wchange.add_reaction('📕')
        await wchange.add_reaction('📙')
        await wchange.add_reaction('📗')
        while True:
            redbook = ['📕']
            orangebook = ['📙']
            greenbook = ['📗']
            plusemoji = ['➕']
            minusemoji = ['➖']
            timeout = 120
            reaction, user = await bot.wait_for('reaction_add')
            timeout
            if reaction.message.id == wchange.id and user.bot is not True:
                if str(reaction.emoji) in redbook:
                    await reaction.message.remove_reaction('📕', user)
                    embed = discord.Embed(title=f"What sort of change do you wish to make to {member.display_name}'s stats?",
                                        description=f"React with to ➖ subtract {amount} XP or with ➕ to add {amount} XP to {member.display_name}'s stats.", color=embcolor)
                    pmmsg = await ctx.send(embed=embed)
                    await pmmsg.add_reaction('➕')
                    await pmmsg.add_reaction('➖')
                    while True:
                        reaction, user = await bot.wait_for('reaction_add')
                        if reaction.message.id == pmmsg.id and user.bot is not True:
                            if user != ctx.message.author:
                                pass
                            else:
                                if str(reaction.emoji) in plusemoji:
                                    add_xp(member.id, amount)
                                    await ctx.send(f"✅ Added {amount} to {member.display_name}'s stats")
                                if str(reaction.emoji) in minusemoji:
                                    remove_xp(member.id, amount)
                                    await ctx.send(f"✅ Removed {amount} to {member.display_name}'s stats")
                if str(reaction.emoji) in orangebook:
                    await reaction.message.remove_reaction('📙', user)
                    embed = discord.Embed(title=f"What sort of change do you wish to make to {member.display_name}'s stats?",
                                        description=f"React with to ➖ subtract {amount} Sytes with ➕ to add {amount} Sytes to {member.display_name}'s stats.", color=embcolor)
                    pmmsg = await ctx.send(embed=embed)
                    await pmmsg.add_reaction('➕')
                    await pmmsg.add_reaction('➖')
                    while True:
                        reaction, user = await bot.wait_for('reaction_add')
                        if reaction.message.id == pmmsg.id and user.bot is not True:
                            if user != ctx.message.author:
                                pass
                            else:
                                if str(reaction.emoji) in plusemoji:
                                    add_tk(member.id, amount)
                                    await ctx.send(f"✅ Added {amount} Sytes to {member.display_name}'s stats")
                                if str(reaction.emoji) in minusemoji:
                                    remove_tk(member.id, amount)
                                    await ctx.send(f"✅ Removed {amount} Sytes to {member.display_name}'s stats")
                if str(reaction.emoji) in greenbook:
                    await reaction.message.remove_reaction('📗', user)
                    boost = getbooster(member.id)
                    if boost == False:
                        setbooster(member.id, True)
                        await ctx.send(f"✅ Set {member.display_name}'s booster status to True")
                    if boost == True:
                        setbooster(member.id, True)
                        await ctx.send(f"✅ Set {member.display_name}'s booster status to False")

@bot.command(pass_context=True)
async def pfp(ctx, member: discord.Member):
    if member == None:
        member = ctx.message.author
    embed = discord.Embed(title="The user's profile picture.", color=embcolor)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role(561266182578110474)
async def purge(ctx, amount: int):
    ongoingpurge = True
    channel = bot.get_channel(logChannel)
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=f"A message purge has occurred!",
                            description="Everything is nice and clean now!", color=embcolor)
    embed.add_field(name=":recycle: Number of messages purged:",
                    value=f"{amount}", inline=False)
    embed.add_field(name=":closed_lock_with_key: Moderator:",
                    value=ctx.message.author.display_name, inline=False)
    embed.set_thumbnail(
        url="https://www.allaboutlean.com/wp-content/uploads/2015/03/Broom-Icon.png")
    # log
    await channel.send(embed=embed)
    ongoingpurge = False


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} messages got deleted.")

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))


@bot.command()
@commands.has_role(566249728732561410)
async def checkuser(ctx, member : discord.Member = None):
    member = ctx.author if not member else member

    roles = [role for role in member.roles]

    embed = discord.Embed(colour=embcolor,
                          timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    
    embed.add_field(name=":desktop: ID:", value=member.id, inline=False)

    embed.add_field(name=":star2: Joined at:", value=member.joined_at.strftime(
        "%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=":date: Created at:", value=member.created_at.strftime(
        "%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=":bust_in_silhouette: Nickname:",
                    value=member.display_name, inline=False)
    
    embed.add_field(name=":robot: Is Bot:", value=member.bot)

    embed.add_field(name="Roles:", value=" ".join(
        [role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def skin(ctx, username = ""):
        uid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        data = uid.json()
        uid = f"{data['id']} "
        embed = discord.Embed(color=embcolor)
        final_uid = uid.replace(' ', '')
        url = f"https://minotar.net/body/{final_uid}/100.png"
        print(url)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def genpw(ctx):
    pw = secrets.token_urlsafe(5)
    await ctx.author.send(ctx.message.author, f"Your generated password is `{pw}`, this password is secure and hasn't been shared with anybody else")

# bot.command()
# async def shop(ctx):

# bot.command()
# async def buy(ctx):

@bot.command()
@commands.has_role(566249728732561410)
async def ban(ctx, member: discord.Member, *, reason='No reason provided.'):
    dm = discord.Embed(title="You have been banned from `SyteSpace`!",
                        description="Details about the ban:", color=embcolor)
    dm.add_field(name=":closed_lock_with_key: Moderator:",
                    value=ctx.message.author.display_name)
    dm.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
    dm.set_thumbnail(url=member.avatar_url)
    logEmb = discord.Embed(
        title="Ban Issued!", description="Details about the ban:", color=embcolor)
    logEmb.add_field(name="Moderator:",
                        value=f"{ctx.message.author.display_name}")
    logEmb.add_field(name=":spy: member Banned:",
                        value=f"{member.name}")
    logEmb.add_field(name=":notepad_spiral: Reason:",
                        value=f"{reason}")
    logEmb.set_thumbnail(url=member.avatar_url)
    log = bot.get_channel(logChannel)
    await member.send(embed=dm)  # Send DM
    await member.ban(reason=reason)  # Ban
    await log.send(embed=logEmb)  # Send To Log
    await ctx.message.delete()  # Delete The Message
    await ctx.send('✅ Moderation action completed')


@bot.command()
@commands.has_role(566249728732561410)
async def warn(ctx, member: discord.Member, *, reason='No reason provided.'):
    embed = discord.Embed(title = "You have been warned in `SyteSpace`!", description = "Details about the warn:", color =0x363942)
    embed.add_field(name = ":closed_lock_with_key: Moderator:", value = ctx.message.author.display_name)
    embed.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
    embed.set_thumbnail(url=member.avatar_url)
    await member.send(embed=embed)# DM it!
    emb = discord.Embed(title = "Warn Issued!", description = "Details about the warn:", color =0x363942)
    emb.add_field(name = "Moderator:", value = f"{ctx.message.author.display_name}")
    emb.add_field(name = ":spy: member Warned:", value = f"{member.name}")
    emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
    emb.set_thumbnail(url=member.avatar_url)
    await log.send(embed=emb)#log it!
    await ctx.send('✅ Moderation action completed')


@bot.command()
@commands.has_role(566249728732561410)
async def kick(ctx, member: discord.Member, *, reason='No reason provided.'):
    dm = discord.Embed(
        color=embcolor, title="You have been kicked from `SyteSpace`!")
    dm.set_thumbnail(url=member.avatar_url)
    dm.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
    dm.add_field(name="Moderator:",
                    value=ctx.message.author.display_name)
    logEmb = discord.Embed(
        color=embcolor, title="A kick has been issued")
    logEmb.add_field(name=":notepad_spiral: Reason:",
                        value=f"{reason}")
    logEmb.add_field(name="Moderator:",
                        value=ctx.message.author.display_name)
    logEmb.add_field(name=":spy: User Kicked:", value=f"{member.name}")
    logEmb.set_thumbnail(url=member.avatar_url)
    log = bot.get_channel(logChannel)
    await member.send(embed=dm)  # Send DM
    await member.kick(reason=reason)  # Kick
    await log.send(embed=logEmb)  # Send To Log
    await ctx.message.delete()  # Delete The Message
    await ctx.send('✅ Moderation action completed')

@bot.command()
@commands.has_role(566249728732561410)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            #dm = discord.Embed(
                #color=embcolor, title="You have been unbanned from `SyteSpace`!")
            #dm.add_field(name="Moderator:",
                        #value=ctx.message.author.display_name)
            #logEmb = discord.Embed(
                #color=embcolor, title="An unban has been issued")
            #logEmb.add_field(name="Moderator:",
                            #value=ctx.message.author.display_name)
            #logEmb.add_field(name=":spy: User Unbanned:", value=f"{member.name}")
            #log = bot.get_channel(logChannel)
            await ctx.send('✅ Moderation action completed')
            #await member.send(embed=dm)  # Send DM
            #await log.send(embed=logEmb)  # Send To Log
            #await ctx.message.delete()  # Delete The Message
            return

@bot.command()
@commands.has_role(566249728732561410)
async def mute(ctx, member: discord.Member = None, *, reason='No reason provided.'):
    role = discord.utils.get(ctx.guild.roles, name="muted")
    unrole = discord.utils.get(ctx.guild.roles, name="👤 Guest")
    if not member:
        await ctx.send("Please specify a member.")
        return
    dm = discord.Embed(
        color=embcolor, title="You have been muted in `SyteSpace`!")
    dm.set_thumbnail(url=member.avatar_url)
    dm.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
    dm.add_field(name="Moderator:",
                value=ctx.message.author.display_name)
    logEmb = discord.Embed(
        color=embcolor, title="A mute has been issued")
    logEmb.add_field(name=":notepad_spiral: Reason:",
                    value=f"{reason}")
    logEmb.add_field(name="Moderator:",
                    value=ctx.message.author.display_name)
    logEmb.add_field(name=":spy: User Muted:", value=f"{member.name}")
    logEmb.set_thumbnail(url=member.avatar_url)
    log = bot.get_channel(logChannel)
    await member.send(embed=dm)  # Send DM
    await member.add_roles(role)
    await member.remove_roles(unrole)
    await log.send(embed=logEmb)  # Send To Log
    await ctx.message.delete()  # Delete The Message
    await ctx.send("✅ Moderation action completed")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command()
@commands.has_role(566249728732561410)
async def unmute(ctx, member: discord.Member = None, *, reason='No reason provided.'):
    role = discord.utils.get(ctx.guild.roles, name="muted")
    unrole = discord.utils.get(ctx.guild.roles, name="guest")
    if not member:
        await ctx.send("Please specify a member.")
        return
    dm = discord.Embed(
        color=embcolor, title="You have been unmuted in `SyteSpace`!")
    dm.set_thumbnail(url=member.avatar_url)
    dm.add_field(name=":notepad_spiral: Reason:", value=f"{reason}")
    dm.add_field(name="Moderator:",
                value=ctx.message.author.display_name)
    logEmb = discord.Embed(
        color=embcolor, title="An unmute has been issued")
    logEmb.add_field(name=":notepad_spiral: Reason:",
                    value=f"{reason}")
    logEmb.add_field(name="Moderator:",
                    value=ctx.message.author.display_name)
    logEmb.add_field(name=":spy: User Unmuted:", value=f"{member.name}")
    logEmb.set_thumbnail(url=member.avatar_url)
    log = bot.get_channel(logChannel)
    await member.send(embed=dm)  # Send DM
    await member.remove_roles(role)
    await member.add_roles(unrole)
    await log.send(embed=logEmb)  # Send To Log
    await ctx.message.delete()  # Delete The Message
    await ctx.send("✅ Moderation action completed")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="What Information Do You Require?",
                          description="React with 💬 for a list of user commands, 🐶 for a list of animal commands and 🛑 for a list of moderation commands", color=embcolor)
    startmsg = await ctx.send(embed=embed)
    await startmsg.add_reaction('💬')
    await startmsg.add_reaction('🛑')
    await startmsg.add_reaction('🐶')
    while True:
        houseemoji = ['🏠']
        chatemoji = ['💬']
        blockemoji = ['🛑']
        dogemoji = ['🐶']
        xemoji = ['❌']
        timeout = 120
        reaction, user = await bot.wait_for('reaction_add')
        timeout
        if reaction.message.id == startmsg.id and user.bot is not True:
            if str(reaction.emoji) in houseemoji:
                await reaction.message.remove_reaction('🏠', user)
                embed = discord.Embed(title="What Information Do You Require?",
                                      description="React with 💬 for a list of user commands, 🐶 for a list of animal commands and 🛑 for a list of moderation commands", color=embcolor)
                await startmsg.edit(embed=embed)
                await startmsg.add_reaction('❌')
            if str(reaction.emoji) in chatemoji:
                await reaction.message.remove_reaction('💬', user)
                await startmsg.add_reaction('🏠')
                await startmsg.add_reaction('❌')
                with open("textfiles/usercmds.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu",
                                          description="`[] = Not Required Argument`, `<> = Required Argument`", color=embcolor)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(
                        text=f"Request by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    await startmsg.edit(embed=embed)
                    await startmsg.add_reaction('❌')
                    txtfile.close()
            if str(reaction.emoji) in dogemoji:
                await reaction.message.remove_reaction('🐶', user)
                await startmsg.add_reaction('🏠')
                with open("textfiles/animal.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu",
                                          description="`[] = Not Required Argument`, `<> = Required Argument`", color=embcolor)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(
                        text=f"Request by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    await startmsg.edit(embed=embed)
                    await startmsg.add_reaction('❌')
                    txtfile.close()
            if str(reaction.emoji) in blockemoji:
                await reaction.message.remove_reaction('🛑', user)
                await startmsg.add_reaction('🏠')
                with open("textfiles/moderation.txt", "r") as txtfile:
                    content = txtfile.read()
                    embed = discord.Embed(title="Help - React with 🏠 to return to the main menu",
                                          description="`[] = Not Required Argument`, `<> = Required Argument`", color=embcolor)
                    embed.add_field(name="\u200b", value=f"{content}")
                    embed.set_footer(
                        text=f"Request by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    await startmsg.edit(embed=embed)
                    await startmsg.add_reaction('❌')
                    txtfile.close()
            if str(reaction.emoji) in xemoji:
                await startmsg.remove_reaction('❌', user)
                await startmsg.delete()


@bot.command()
@commands.has_role(561266182578110474)
async def weekly_reset(ctx):
    for x in ctx.members:
        uid = x.id
        reset_weeklymessages(uid)
        print(f"[Activity] Reset weekly for {uid}")

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
        bot_ping = round(bot.latency * 1000 / 2)
        embed = discord.Embed(title="Connection Statistics", description="Current Connection Statistics", color=embcolor)
        embed.add_field(name="Ping (st)", value="`%sms`" % ping, inline=False)
        embed.add_field(name="Ping (heartbeat)", value="`%sms`" % bot_ping, inline=False)
        embed.add_field(name="Server Used", value="`%s`" % host, inline=False)
        embed.add_field(name="Download", value="`%s mbps`" % down, inline=False)
        embed.add_field(name="Upload", value="`%s mbps`" % up, inline=False)
        embed.add_field(name="Google", value="`%sms`" % google, inline=False)
        embed.add_field(name="Cloudflare", value="`%sms`" % cloudflare, inline=False)
        embed.set_footer(text=f"Requested by: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

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
        if currentlvl != 20:
            set_lvl(uid, 10)
        else:
            pass


def create_user_if_not_exists(user_id: str):
    c.execute("SELECT COUNT(*) FROM Users WHERE UserID=%s", (str(user_id),))
    user_count = c.fetchone()[0]
    if user_count < 1:
        print("[Users Table]Creating user with id " + str(user_id))
        c.execute("INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)",
                  (str(user_id), 0, 0, 0, 0, 0))
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
        c.execute("INSERT INTO Activity VALUES (%s, %s, %s, %s, %s)",
                  (str(user_id), 0, 0, 0, 0))
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


def setbooster(user_id: str, setto=bool):
    c.execute("UPDATE Ecopp SET Boost=%s WHERE UserID=%s",
              (bool(setto), str(user_id)))
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
    c.execute("SELECT GlobalMessages FROM Activity WHERE UserID=%s",
              (str(user_id),))
    user_globalmessages = int(c.fetchone()[0])
    db.commit()
    return user_globalmessages


def get_weeklymessages(user_id: str):
    create_activity(user_id)
    c.execute("SELECT WeeklyMessages FROM Activity WHERE UserID=%s",
              (str(user_id),))
    user_weeklymessages = int(c.fetchone()[0])
    db.commit()
    return user_weeklymessages


def reset_weeklymessages(user_id: str):
    create_activity(user_id)
    c.execute("UPDATE Activity SET WeeklyMessages=%s WHERE UserID=%s",
              (0, str(user_id)))
    db.commit()
    return True


def set_weekly_rank(user_id, rank: int):
    c.execute("UPDATE Activity SET WeeklyRank=%s WHERE UserID=%s",
              (rank, str(user_id)))
    db.commit()
    return rank


def get_user_rank(input_rank: int):
    c.execute("SELECT UserID FROM Activity WHERE WeeklyRank=%s",
              (int(input_rank),))
    rank = int(c.fetchone()[0])
    db.commit()
    return rank


def add_messages(user_id: str):
    create_activity(user_id)
    globalmsg = int(get_globalmessages(user_id) + 1)
    weeklymsg = int(get_weeklymessages(user_id) + 1)
    c.execute("UPDATE Activity SET GlobalMessages=%s WHERE UserID=%s",
              (int(globalmsg), str(user_id)))
    c.execute("UPDATE Activity SET WeeklyMessages=%s WHERE UserID=%s",
              (int(weeklymsg), str(user_id)))
    db.commit()
    return globalmsg + weeklymsg


def isrisk(creation_date):
    inputacc = datetime.utcnow() - creation_date
    accagedays = int(inputacc.days)
    if accagedays <= 7:
        return True
    else:
        return False

def get_ticknumb():
    c.execute("SELECT Number FROM Tickets")
    row = c.fetchone()
    if row is not None: 
        ticknumb = row[0]
    else:
        print("[ERROR] Reverting to 1 as a ticketnumber")
        ticknumb = 1
    db.commit()
    return ticknumb

def setup_ticknumb():
    c.execute("UPDATE Tickets SET Number=%s", (int(0), ))
    db.commit()
    return get_ticknumb()

def update_ticknumb():
    current = get_ticknumb()
    new = current + 1
    c.execute("UPDATE Tickets SET Number=%s", (int(new), ))
    db.commit()
    return new


async def chng_pr():
    await bot.wait_until_ready()
    statuses = ["s!help", "with the fate of the world", "with hosting", "Minecraft", f"with {len(list(bot.get_all_members()))} users"]
    statuses = cycle(statuses)
    while not bot.is_closed():
        status = next(statuses)
        await bot.change_presence(activity=discord.Game(status), status='idle')
        await asyncio.sleep(15)
bot.loop.create_task(chng_pr())

async def warnuser(user, warnedby, reason, msg):
    try:
        log = bot.get_channel(logChannel)
        embed = discord.Embed(title = "You have been warned in `SyteSpace`!", description = "Details about the warn:", color =0x363942)
        embed.add_field(name = ":closed_lock_with_key: Moderator:", value = warnedby.display_name)
        embed.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
        embed.set_footer(text="This action was preformed by the overwatch auto-moderation system, if you belive this is a mistake please contact a member of staff", icon_url="https://images-ext-2.discordapp.net/external/uRBzAE1kdh2IHBCpPtO876DgohZkZDafXCfeH0mKu_s/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/534445908394377226/0dcc56c5fb681d249c94bbd929afbcbc.webp")
        embed.set_thumbnail(url=member.avatar_url)
        await member.send(embed=embed)# DM it!
        emb = discord.Embed(title = "Warn Issued!", description = "Details about the warn:", color =0x363942)
        emb.add_field(name = "Moderator:", value = f"{warnedby.display_name}")
        emb.add_field(name = ":spy: member Warned:", value = f"{member.name}")
        emb.add_field(name = ":notepad_spiral: Reason:", value = f"{reason}")
        emb.set_thumbnail(url=member.avatar_url)
        await log.send(embed=emb)#log it!
    except:
        pass


async def urldetection(msg):
    log = bot.get_channel(logChannel)
    urls = re.findall(urlregex, msg.content.lower())
    api = open("API.TXT", "r").read()
    if len(urls) <= 0:
        return False
    if msg.channel == log:
        return False
    else:
        await msg.delete()
        await msg.send("{}, URLs are not allowed!".format(msg.author.mention), delete_after=10)
        await bot.get_channel(610156083259899904).send("{} said a URL in {}:```{}```".format(msg.author.mention, msg.channel.mention, msg.content.lower().replace("`", "")))
        if msg.author.id in blockedurls:
            if len([i for i in blockedurls[msg.author.id] if i + timedelta(hours=1) > datetime.utcnow()]) >= 2:
                await warnuser(msg.author, bot.user, "URL Spam", msg)
            blockedurls[msg.author.id].append(datetime.utcnow())
            return
        else:
            blockedurls[msg.author.id] = [datetime.utcnow()]
        for i in set(urls):
            res = requests.get(f"https://api.builtwith.com/free1/api.json?KEY={api}&LOOKUP={i}")
            if "adult" in [i['name'] for i in [i[0] for i in [i['categories'] for i in res.json()['groups'] if "categories" in i] if i] if "name" in i]:
                await warnuser(msg.author, bot.user, "Inappropriate Content", msg)
                return True
    return True

@bot.event
async def on_message_delete(message):
    try:
        if message.author == bot.user:
            pass
        elif message.content.startswith('s!'):
            pass
        elif ongoingpurge == True:
            pass
        else:
            log = bot.get_channel(logChannel)
            content = message.content
            author_name = message.author.display_name
            embed = discord.Embed(
                title=f"A message has been deleted!", color=embcolor)
            embed.add_field(name=":notepad_spiral: Message Content:",
                            value=f"{content}", inline=False)
            embed.add_field(name=":spy: Message Sender:",
                            value=f"{author_name}", inline=False)
            embed.add_field(name=":tv: Message Channel",
                            value=f"<#{message.channel.id}>")
            embed.set_thumbnail(
                url="http://icons.iconarchive.com/icons/ramotion/custom-mac-os/512/Trash-empty-icon.png")
            # log
            await log.send(embed=embed)
    except discord.errors.HTTPException:
        pass

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(logChannel)
    try:
        before_content = before.content
        after_content = after.content
        if before_content == after_content:
            pass
        else:
            embed = discord.Embed(
                title=f"A message has been edited!", color=embcolor)
            embed.add_field(name=":notepad_spiral: Before:",
                            value=f"{before_content}", inline=True)
            embed.add_field(name=":notepad_spiral: After:",
                            value=f"{after_content}", inline=True)
            embed.add_field(name=":spy: Message Sender:",
                            value=f"{before.author.display_name}", inline=False)
            embed.add_field(name=":spy: Message Sender ID:",
                            value=f"{before.author.id}", inline=False)
            embed.add_field(name=":tv: Message Channel",
                            value=f"<#{before.channel.id}>")
            embed.set_thumbnail(
                url="https://www.freeiconspng.com/uploads/edit-icon-orange-pencil-0.png")
            # log
            await channel.send(embed=embed)
    except discord.errors.HTTPException:
        pass


@bot.event
async def on_member_remove(member: discord.Member):
    channel = bot.get_channel(logChannel)
    sec = discord.Embed(title=f"A user has left!", color=embcolor)
    sec.add_field(name=":notepad_spiral: User Name:",
                  value=f"{member.display_name}", inline=True)
    sec.add_field(name=":space_invader:  User ID:",
                  value=f"{member.id}", inline=False)
    sec.add_field(name=":robot: Is Bot", value=f"{member.bot}", inline=False)
    sec.add_field(name=":clock1: Joined Server at", value=member.joined_at.__format__(
        '%A, %d. %B %Y @ %H:%M:%S'), inline=False)
    sec.set_thumbnail(url=member.avatar_url)
    # log
    await channel.send(embed=sec)

@bot.command()
@commands.has_role(561266182578110474)
async def shutdown(ctx):
        await ctx.send("I have logged out.")
        await ctx.bot.logout()
        
@bot.event
async def on_member_join(member: discord.Member):
    #Security
    risky = isrisk(member.created_at)
    log = bot.get_channel(logChannel)
    if risky == True:
        log = bot.get_channel(logChannel)
        create_user_if_not_exists(member.id)
        guest = discord.utils.get(member.guild.roles, name="👤 Guest")
        await member.add_roles(guest, reason = "Autorole")
        embed = discord.Embed(title = f"Welcome to the syte.space discord server, {member.display_name}!", description = "If you wish to aquire a Minecraft server please check out <#550958398410194974> and open a ticket by doing `s!new`", color=embcolor)
        embed.set_footer(text=f"We now have {member.guild.member_count} members")
        embed.set_thumbnail(url=member.avatar_url)
        welcome = bot.get_channel(welcomeChannel)
        welcome_message = await welcome.send(embed=embed)
        await welcome_message.add_reaction('🇭')
        await welcome_message.add_reaction('🇮')
        sec = discord.Embed(title=f"A user has joined! [HIGH RISK]", color=0xff0000)
        sec.add_field(name=":notepad_spiral: User Name:", value=f"{member.display_name}", inline=True)
        sec.add_field(name=":space_invader:  User ID:", value=f"{member.id}", inline=False)
        sec.add_field(name=":robot: Is Bot", value=f"{member.bot}", inline=False)
        sec.add_field(name=":clock1: Account Creation Datetime (UTC)", value=f"{member.created_at}", inline=False)
        sec.add_field(name=":rotating_light:", value="HIGH RISK ACCOUNT - STAFF PLEASE MONITOR")
        sec.set_thumbnail(url=member.avatar_url)
        await log.send("@here High Risk Account, Please Monitor")
        await log.send(embed=sec)#log
    elif risky == False:
        log = bot.get_channel(logChannel)
        create_user_if_not_exists(member.id)
        guest = discord.utils.get(member.guild.roles, name="👤 Guest")
        await member.add_roles(guest, reason = "Autorole")
        embed = discord.Embed(title = f"Welcome to the syte.space discord server, {member.display_name}!", description = "If you wish to aquire a Minecraft server please check out <#550958398410194974> and open a ticket by doing `s!new`", color=embcolor)
        embed.set_footer(text=f"We now have {member.guild.member_count} members")
        embed.set_thumbnail(url=member.avatar_url)
        welcome = bot.get_channel(welcomeChannel)
        welcome_message = await welcome.send(embed=embed)
        await welcome_message.add_reaction('🇭')
        await welcome_message.add_reaction('🇮')
        sec = discord.Embed(title=f"A user has joined!!", color=embcolor)
        sec.add_field(name=":notepad_spiral: User Name:", value=f"{member.display_name}", inline=True)
        sec.add_field(name=":space_invader:  User ID:", value=f"{member.id}", inline=False)
        sec.add_field(name=":robot: Is Bot", value=f"{member.bot}", inline=False)
        sec.add_field(name=":clock1: Account Creation Datetime (UTC)", value=f"{member.created_at}", inline=False)
        sec.set_thumbnail(url=member.avatar_url)
        await log.send(embed=sec)#log

@bot.event
async def on_message(message):
    create_economypp(message.author.id)
    create_activity(message.author.id)
    boost = getbooster(message.author.id)
    await urldetection(message)
    ping = False
    if len(message.raw_mentions) + len(message.raw_role_mentions) > 0:
        ping = True
    if message.author.id in spams:
        if ping:
            spams[message.author.id]['pings'].append([message, datetime.utcnow()])
        spams[message.author.id]['msgs'].append([message, datetime.utcnow()])
    else:
        if ping:
            spams[message.author.id] = {"pings": [[message, datetime.utcnow()]], "msgs": [[message, datetime.utcnow()]]}
        else:
            spams[message.author.id] = {"pings": [], "msgs": [[message, datetime.utcnow()]]}
    if boost == True:
        if_tk_boost = secrets.choice([True, False])
        if if_tk_boost == True:
            amount = int(random.randint(1, 5))
            add_tk(message.author.id, amount)
        else:
            pass
    elif boost == False:
        if_tk = secrets.choice([True, False, False, False, False])
        if if_tk == True:
            add_tk(message.author.id, 1)
        else:
            pass
    await bot.process_commands(message)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Welp! Adam must of defined a global variable!",
                              description=f"The command `{ctx.invoked_with}` was not found! We suggest you do `s!help` to see all of the commands",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRole):
        embed = discord.Embed(title="Welp! Adam must of defined a global variable!",
                              description=f"You don't have permission to execute `{ctx.invoked_with}`.",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Welp! Adam must of defined a global variable!",
                              description=f"`{error}`",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
        raise error


bot.run(TOKEN)
