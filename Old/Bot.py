import datetime, discord, requests, asyncio, img2pdf, PyPDF4, random, json, math, time, PIL, os
from PyPDF4 import PdfFileWriter, PdfFileReader
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from datetime import timedelta
from datetime import datetime as dt
from discord.utils import get

client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
client.remove_command('help')
os.chdir("./Imperum")
groups = "jsondbs/groups.json"
whitelist = "jsondbs/whitelist.json"
docs = "jsondbs/docs.json"

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="nUSA"))
    print('Imperum now online!')
    print(f'Running with {round(client.latency * 1000)}ms ping.')

@client.event
async def on_message(msg):
    if msg.content.lower() == "!upload":
        whitelisted = False
        with open(whitelist, "r+") as f:
            data = json.load(f)
            if int(msg.author.id) in data["whitelist"]:
                whitelisted = True
        response = await msg.reply("<a:loading:1011088285998776372>")
        if whitelisted == True:

            def check(m):
                return m.author == msg.author
            
            await response.edit(content="Send your document (PDF)")
            getfile = await client.wait_for('message', check=check)

            files = getfile.attachments
            if files == []:
                await response.edit(content="You need to upload a document")
            elif len(files) > 1:
                await response.edit(content="You can only send one file at a time")
            elif len(files) == 1:
                thefile = files[0]
            await getfile.delete()
            if thefile.content_type != "application/pdf":
                await response.edit(content="You can only upload a PDF File")
            else:

                await response.edit(content="Which clearances can access\n(New line per agency)")
                getclearances = await client.wait_for('message', check=check)

                noncapclearances = getclearances.content.split("\n")
                await getclearances.delete()
                clearances = []
                for el in noncapclearances:
                    clearances.append(el.upper())
                allclearances = ["PUBLIC", "WASHTOW", "FRB", "USCP", "MPD", "BUS", "BOP", "DOT", "DSS", "DOTT", "CSPAN", "DIA", "FRP", "SF", "DFPA", "FBI", "USM", "DOCAL", "USMS", "CIA", "NSA", "DCCC", "FPS", "JB", "SWAT", "SS", "DHS", "DOD", "DOS", "WHS", "DOJ", "TTS", "WF", "TAXI", "DCEMS", "DCFD"]
                invalids = []
                valid = True
                for el in clearances:
                    if el not in allclearances:
                        invalids.append(el)
                        valid = False
                publicand = False
                if "PUBLIC" in clearances:
                    if len(clearances) > 1:
                        valid = False
                        publicand = True
                if valid == True:
                    selfiscleared = True
                    selfnotclearedto = []
                    with open(whitelist, "r+") as f:
                        data = json.load(f)
                        if clearances[0] == "PUBLIC":
                            selfiscleared = True
                        if int(msg.author.id) in data["administration"]:
                            selfiscleared = True
                        else:
                            if str(msg.author.id) in data["clearances"]:
                                for el in clearances:
                                    if el not in data["clearances"][str(msg.author.id)]:
                                        selfnotclearedto.append(el)
                                        selfiscleared = False
                            else:
                                selfiscleared = False
                    if selfiscleared == True:
                        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        rngid = f"{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}"
                        await thefile.save(f"docs/{rngid}.pdf")
                        with open(docs, "r+") as f:
                            data = json.load(f)
                            while rngid in data["docs"]:
                                rngid = f"{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}"
                            utctimenow = dt.utcnow()
                            utctimenowformatted = utctimenow.strftime("%d/%m/%Y %H:%M")
                            data["docs"][rngid] = {
                                "name": thefile.filename.rstrip(".pdf"),
                                "author": int(msg.author.id),
                                "clearance": [],
                                "upload": utctimenowformatted
                            }
                            for el in clearances:
                                data["docs"][rngid]["clearance"].append(el)
                            f.seek(0)
                            f.truncate()
                            json.dump(data, f, indent=4)
                        await response.edit(content=f"Submitted with ID:`{rngid}`")
                    else:
                        allselfnotclearedto = ""
                        for el in selfnotclearedto:
                            allselfnotclearedto = f"{allselfnotclearedto}{el}\n"
                        allselfnotclearedto = allselfnotclearedto.rstrip("\n")
                        await response.edit(content=f"You don't have the following clearances you're attempting to upload to:```\n{allselfnotclearedto}\n```")
                elif publicand == True:
                    await response.edit(content="You can't upload to `PUBLIC` and other clearances")
                else:
                    invalidresponse = ""
                    for el in invalids:
                        invalidresponse = f"{invalidresponse}{el}\n"
                    invalidresponse = invalidresponse.rstrip("\n")
                    await response.edit(content=f"The following clearances do not exist:```\n{invalidresponse}\n```")
        else:
            await response.edit(content="Not whitelisted")
    await client.process_commands(msg)

@client.command()
async def basic(ctx, *, who):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        user = requests.get("https://api.roblox.com/users/get-by-username", params={"username": who})
        userresponse = json.loads(user.text)
        if "success" in userresponse:
            if userresponse["success"] == False:
                skip = False
                try:
                    who = int(who)
                except:
                    skip = True
                if skip == False:
                    user = requests.get(f"https://api.roblox.com/users/{who}")
                    userresponse = json.loads(user.text)
                    if "errors" in userresponse:
                        await msg.edit(content="Invalid Username/ID")
                    else:
                        userid = userresponse["Id"]
                        username = userresponse["Username"]
                        gotuser = True
                else:
                    await msg.edit(content="Invalid Username/ID")
        else:
            userid = userresponse["Id"]
            username = userresponse["Username"]
            gotuser = True
        if gotuser == True:
            getnick = requests.get(f"https://users.roblox.com/v1/users/{userid}")
            getnickresponse = json.loads(getnick.text)
            usernick = getnickresponse["displayName"]
            embed = discord.Embed(
                title=username,
                colour=0x000000,
                description=f"**Id:**{userid}\n**Nick:**{usernick}\n**Profile:**[Link](https://www.roblox.com/users/{userid}/profile)"
            )
            embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
            await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def employment(ctx, *, who):
    whitelisted, gotuser = False, False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        user = requests.get("https://api.roblox.com/users/get-by-username", params={"username": who})
        userresponse = json.loads(user.text)
        if "success" in userresponse:
            if userresponse["success"] == False:
                skip = False
                try:
                    who = int(who)
                except:
                    skip = True
                if skip == False:
                    user = requests.get(f"https://api.roblox.com/users/{who}")
                    userresponse = json.loads(user.text)
                    if "errors" in userresponse:
                        await msg.edit(content="Invalid Username/ID")
                    else:
                        userid = userresponse["Id"]
                        username = userresponse["Username"]
                        gotuser = True
                else:
                    await msg.edit(content="Invalid Username/ID")
        else:
            userid = userresponse["Id"]
            username = userresponse["Username"]
            gotuser = True
        if gotuser == True:
            usergroups = requests.get(f"https://groups.roblox.com/v2/users/{userid}/groups/roles")
            usergroupsresponse = json.loads(usergroups.text)
            nusagroups = {}
            with open(groups, "r+") as f:
                data = json.load(f)
                for el in usergroupsresponse["data"]:
                    for foo in data["groups"]:
                        if el["group"]["id"] == data["groups"][foo]["groupid"]:
                            nusagroups[foo] = el["role"]["name"]
            embed = discord.Embed(
                title=f"{username} - Employment",
                colour=0x000000,
                description=""
            )
            embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
            for el in nusagroups:
                embed.add_field(name=el, value=nusagroups[el], inline=False)
            if len(embed.fields) == 0:
                embed.description = "N/A"
            await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def bgc(ctx, *, who):
    whitelisted, gotuser = False, False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        user = requests.get("https://api.roblox.com/users/get-by-username", params={"username": who})
        userresponse = json.loads(user.text)
        if "success" in userresponse:
            if userresponse["success"] == False:
                skip = False
                try:
                    who = int(who)
                except:
                    skip = True
                if skip == False:
                    user = requests.get(f"https://api.roblox.com/users/{who}")
                    userresponse = json.loads(user.text)
                    if "errors" in userresponse:
                        await msg.edit(content="Invalid Username/ID")
                    else:
                        userid = userresponse["Id"]
                        username = userresponse["Username"]
                        gotuser = True
                else:
                    await msg.edit(content="Invalid Username/ID")
        else:
            userid = userresponse["Id"]
            username = userresponse["Username"]
            gotuser = True
        if gotuser == True:
            groupcheck = False
            citizen = False
            fedpris = True
            suspendedcheck = True
            usergroups = requests.get(f"https://groups.roblox.com/v2/users/{userid}/groups/roles")
            usergroupsresponse = json.loads(usergroups.text)
            groupscheck = True
            totalusergroups = 0
            for el in usergroupsresponse["data"]:
                totalusergroups += 1
            with open(groups, "r+") as f:
                data = json.load(f)
                for el in usergroupsresponse["data"]:
                    if el["group"]["id"] == 758071:
                        groupcheck = True
                        if el["role"]["name"] not in ["Immigration Office", "Traitors", "Failed Immigration", "Federal Prisoner"]:
                            citizen = True
                        if el["role"]["name"] == "Federal Prisoner":
                            fedpris = False
                    for foo in data["groups"]:
                        if el["group"]["id"] == data["groups"][foo]["groupid"]:
                            if el["role"]["name"] == data["groups"][foo]["suspendedname"]:
                                suspendedcheck = False
            accountage = requests.get(f"https://users.roblox.com/v1/users/{userid}")
            accountageresponse = json.loads(accountage.text)
            accountageyear = accountageresponse["created"][0] + accountageresponse["created"][1] + accountageresponse["created"][2] + accountageresponse["created"][3]
            accountagemonth = accountageresponse["created"][5] + accountageresponse["created"][6]
            accountageday = accountageresponse["created"][8] + accountageresponse["created"][9]
            accountagestring = f"{accountageday}/{accountagemonth}/{accountageyear} 01:01:01"
            accountageobject = dt.strptime(accountagestring, '%d/%m/%Y %H:%M:%S')
            utctimenow = dt.utcnow()
            accountagefullobject = str(utctimenow - accountageobject)
            accountagefullobject = accountagefullobject.split()[0]
            accountagecheck = True
            if int(accountagefullobject) < 90:
                accountagecheck = False
            friends = requests.get(f"https://friends.roblox.com/v1/users/{userid}/friends/count")
            friendsresponse = json.loads(friends.text)
            friendstotal = friendsresponse["count"]
            friendscheck = True
            if int(friendstotal) < 10:
                friendscheck = False
            followers = requests.get(f"https://friends.roblox.com/v1/users/{userid}/followers/count")
            followersresponse = json.loads(followers.text)
            followerstotal = followersresponse["count"]
            followerscheck = True
            if int(followerstotal) < 5:
                followerscheck = False
            followings = requests.get(f"https://friends.roblox.com/v1/users/{userid}/followings/count")
            followingsresponse = json.loads(followings.text)
            followingstotal = followingsresponse["count"]
            followingscheck = True
            if int(followingstotal) < 5:
                followingscheck = False
            if totalusergroups < 5:
                groupscheck = False
            badges = requests.get(f"https://badges.roblox.com/v1/users/{userid}/badges/?limit=100")
            badgesresponse = json.loads(badges.text)
            badgestotal = 0
            for el in badgesresponse["data"]:
                badgestotal += 1
            badgescheck = True
            if badgestotal < 10:
                badgescheck = False
            embed = discord.Embed(
                title="Background Check",
                colour=0x000000,
                description=""
            )
            embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
            amountfailed = 0
            for el in [groupcheck, citizen, fedpris, suspendedcheck, accountagecheck, friendscheck, followerscheck, followingscheck, groupscheck, badgescheck]:
                if el == False:
                    amountfailed += 1
            if amountfailed > 0:
                embed.description=f"**{username}** has failed Imperum's automatic background check. ({amountfailed}/10 Failed)\nFor a more detailed view, use `!bgcdetail {{user}}`"
            else:
                embed.description=f"**{username}** has passed Imperum's automatic background check. ({amountfailed}/10 Failed)\nFor a more detailed view, use `!bgcdetail {{user}}`"
            await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def bgcdetail(ctx, *, who):
    whitelisted, gotuser = False, False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        user = requests.get("https://api.roblox.com/users/get-by-username", params={"username": who})
        userresponse = json.loads(user.text)
        if "success" in userresponse:
            if userresponse["success"] == False:
                skip = False
                try:
                    who = int(who)
                except:
                    skip = True
                if skip == False:
                    user = requests.get(f"https://api.roblox.com/users/{who}")
                    userresponse = json.loads(user.text)
                    if "errors" in userresponse:
                        await msg.edit(content="Invalid Username/ID")
                    else:
                        userid = userresponse["Id"]
                        username = userresponse["Username"]
                        gotuser = True
                else:
                    await msg.edit(content="Invalid Username/ID")
        else:
            userid = userresponse["Id"]
            username = userresponse["Username"]
            gotuser = True
        if gotuser == True:
            groupcheck = False
            citizen = False
            fedpris = True
            suspendedcheck = True
            amountsuspended = 0
            usergroups = requests.get(f"https://groups.roblox.com/v2/users/{userid}/groups/roles")
            usergroupsresponse = json.loads(usergroups.text)
            groupscheck = True
            totalusergroups = 0
            for el in usergroupsresponse["data"]:
                totalusergroups += 1
            with open(groups, "r+") as f:
                data = json.load(f)
                for el in usergroupsresponse["data"]:
                    if el["group"]["id"] == 758071:
                        groupcheck = True
                        if el["role"]["name"] not in ["Immigration Office", "Traitors", "Failed Immigration", "Federal Prisoner"]:
                            citizen = True
                        elif el["role"]["name"] == "Federal Prisoner":
                            fedpris = False
                    for foo in data["groups"]:
                        if el["group"]["id"] == data["groups"][foo]["groupid"]:
                            if el["role"]["name"] == data["groups"][foo]["suspendedname"]:
                                amountsuspended += 1
            accountage = requests.get(f"https://users.roblox.com/v1/users/{userid}")
            accountageresponse = json.loads(accountage.text)
            accountageyear = accountageresponse["created"][0] + accountageresponse["created"][1] + accountageresponse["created"][2] + accountageresponse["created"][3]
            accountagemonth = accountageresponse["created"][5] + accountageresponse["created"][6]
            accountageday = accountageresponse["created"][8] + accountageresponse["created"][9]
            accountagestring = f"{accountageday}/{accountagemonth}/{accountageyear} 01:01:01"
            accountageobject = dt.strptime(accountagestring, '%d/%m/%Y %H:%M:%S')
            utctimenow = dt.utcnow()
            accountagefullobject = str(utctimenow - accountageobject)
            accountagefullobject = accountagefullobject.split()[0]
            accountagecheck = True
            if int(accountagefullobject) < 90:
                accountagecheck = False
            friends = requests.get(f"https://friends.roblox.com/v1/users/{userid}/friends/count")
            friendsresponse = json.loads(friends.text)
            friendstotal = friendsresponse["count"]
            friendscheck = True
            if int(friendstotal) < 10:
                friendscheck = False
            followers = requests.get(f"https://friends.roblox.com/v1/users/{userid}/followers/count")
            followersresponse = json.loads(followers.text)
            followerstotal = followersresponse["count"]
            followerscheck = True
            if int(followerstotal) < 5:
                followerscheck = False
            followings = requests.get(f"https://friends.roblox.com/v1/users/{userid}/followings/count")
            followingsresponse = json.loads(followings.text)
            followingstotal = followingsresponse["count"]
            followingscheck = True
            if int(followingstotal) < 5:
                followingscheck = False
            if totalusergroups < 5:
                groupscheck = False
            badges = requests.get(f"https://badges.roblox.com/v1/users/{userid}/badges/?limit=100")
            badgesresponse = json.loads(badges.text)
            badgestotal = 0
            for el in badgesresponse["data"]:
                badgestotal += 1
            badgescheck = True
            if badgestotal < 10:
                badgescheck = False
            if amountsuspended > 0:
                suspendedcheck = False
            embed = discord.Embed(
                title="Background Check",
                colour=0x000000,
                description=""
            )
            embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
            amountfailed = 0
            for el in [groupcheck, citizen, suspendedcheck]:
                if el == False:
                    amountfailed += 1
            desc = f"**{username}'s Results:**\n"
            if groupcheck == False:
                desc = f"{desc}<:x_:1013194865150021692> In nUSA Group\n"
            else:
                desc = f"{desc}:white_check_mark: In nUSA Group\n"
            if citizen == False:
                desc = f"{desc}<:x_:1013194865150021692> Citizenship Check\n"
            else:
                desc = f"{desc}:white_check_mark: Citizenship Check\n"
            if fedpris == False:
                desc = f"{desc}<:x_:1013194865150021692> Federal Prisoner Check\n"
            else:
                desc = f"{desc}:white_check_mark: Federal Prisoner Check\n"
            if suspendedcheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Suspended Check (Suspended in {amountsuspended} groups)\n"
            else:
                desc = f"{desc}:white_check_mark: Suspended Check\n"
            if accountagecheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Account Age Check ({accountagefullobject} Days)\n"
            else:
                desc = f"{desc}:white_check_mark: Account Age Check ({accountagefullobject} Days)\n"
            if friendscheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Friends Check ({friendstotal})\n"
            else:
                desc = f"{desc}:white_check_mark: Friends Check ({friendstotal})\n"
            if followerscheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Followers Check ({followerstotal})\n"
            else:
                desc = f"{desc}:white_check_mark: Followers Check ({followerstotal})\n"
            if followingscheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Followings Check ({followingstotal})\n"
            else:
                desc = f"{desc}:white_check_mark: Followings Check ({followingstotal})\n"
            if groupscheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Groups Check ({totalusergroups})\n"
            else:
                desc = f"{desc}:white_check_mark: Groups Check ({totalusergroups})\n"
            if badgescheck == False:
                desc = f"{desc}<:x_:1013194865150021692> Badges Check ({badgestotal})"
            else:
                if badgestotal == 100:
                    badgestotal = "100+"
                desc = f"{desc}:white_check_mark: Badges Check ({badgestotal})"
            embed.description = desc
            await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def index(ctx):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        embed = discord.Embed(
            title="Imperum Document Index",
            colour=0x000000,
            description="The following documents have been uploaded within the past 7 days.\nAll times and dates are in UTC."
        )
        embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
        with open(docs, "r+") as f:
            data = json.load(f)
            for el in data["docs"]:
                uploadtime = data["docs"][el]["upload"]
                uploadtimeobject = dt.strptime(uploadtime, "%d/%m/%Y %H:%M")
                utctimenow = dt.utcnow()
                timediff = utctimenow - uploadtimeobject
                if int(timediff.days) < 7:
                    valuemsg = f"**Id:**{el}\n**Author:**{data['docs'][el]['author']}\n**Upload:**{data['docs'][el]['upload']}\n**Clearances:**"
                    clearancesmsg = ""
                    for foo in data["docs"][el]["clearance"]:
                        clearancesmsg = f"{clearancesmsg}{foo}, "
                    clearancesmsg = clearancesmsg.rstrip(", ")
                    valuemsg = valuemsg+clearancesmsg
                    embed.add_field(name=data["docs"][el]["name"], value=valuemsg)
            await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def mydocs(ctx):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        alldocs = {}
        with open(docs, "r+") as f:
            data = json.load(f)
            for el in data["docs"]:
                if int(data["docs"][el]["author"]) == int(ctx.author.id):
                    alldocs[el] = {
                        "name": data["docs"][el]["name"],
                        "clearance": [],
                        "upload": data["docs"][el]["upload"]
                    }
                    for foo in data["docs"][el]["clearance"]:
                        alldocs[el]["clearance"].append(foo)
        embed = discord.Embed(
            title=f"{ctx.author.name}'s Documents",
            colour=0x000000,
            description=""
        )
        embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
        for el in alldocs:
            allclearances = ""
            for foo in alldocs[el]["clearance"]:
                allclearances = f"{allclearances}{foo}, "
            allclearances = allclearances.rstrip(", ")
            embed.add_field(name=alldocs[el]["name"], value=f"**Id:**{el}\n**Clearances:**{allclearances}\n**Upload:**{alldocs[el]['upload']}")
        await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def view(ctx, *, docid):
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    docexists = False
    with open(docs, "r+") as f:
        data = json.load(f)
        if docid in data["docs"]:
            docexists = True
            reqclearances = data["docs"][docid]["clearance"]
            docname = data["docs"][docid]["name"]
    canview = False
    if docexists == True:
        if "PUBLIC" in reqclearances:
            canview = True
        else:
            currentclearances = []
            with open(whitelist, "r+") as f:
                data = json.load(f)
                admin = False
                if int(ctx.author.id) in data["administration"]:
                    admin = True
                if str(ctx.author.id) in data["clearances"]:
                    for el in data["clearances"][str(ctx.author.id)]:
                        currentclearances.append(el)
            for el in reqclearances:
                for foo in currentclearances:
                    if foo == el:
                        canview = True
                        break
        if canview == True or admin == True:
            ogpdf = PdfFileReader(f"docs/{docid}.pdf")
            ogpdfpage1 = ogpdf.getPage(0)
            pdf_width = int(round(float(ogpdfpage1["/MediaBox"][2])*2.7782))
            pdf_height = int(round(float(ogpdfpage1["/MediaBox"][3])*2.7782))
            watermarkdir = "docs/retrieving/watermark.png"
            pdfdir = "docs/retrieving/watermark.pdf"



            text_to_be_rotated = f"{ctx.author.name}#{ctx.author.discriminator}"
            message_length = len(text_to_be_rotated)

            FONT_RATIO = 1.3
            DIAGONAL_PERCENTAGE = 1
            diagonal_length = int(math.sqrt((pdf_width**2) + (pdf_height**2)))
            diagonal_to_use = diagonal_length * DIAGONAL_PERCENTAGE
            font_size = int(diagonal_to_use / (message_length / FONT_RATIO))
            font = ImageFont.truetype("Futura.ttf", font_size)

            image = Image.new('RGBA', (pdf_width, pdf_height), (0, 0, 0, 0))

            mark_width, mark_height = font.getsize(text_to_be_rotated)
            watermark = Image.new('RGBA', (mark_width, mark_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            draw.text((0, 0), text=text_to_be_rotated, font=font, fill=(255, 0, 0, int(125.5)))
            angle = math.degrees(math.atan(-(pdf_height/pdf_width)))
            watermark = watermark.rotate(angle, expand=1)

            wx, wy = watermark.size
            px = int((pdf_width - wx)/2)
            py = int((pdf_height - wy)/2)
            image.paste(watermark, (px, py, px + wx, py + wy), watermark)

            image.save(watermarkdir)
            image.close()



            image = Image.open(watermarkdir)

            with open(pdfdir,"wb") as f:
                f.write(img2pdf.convert(image.filename))

            pdf = PyPDF4.PdfFileReader(pdfdir)
            page0 = pdf.getPage(0)
            page0.scaleBy(0.5)
            writer = PyPDF4.PdfFileWriter()
            writer.addPage(page0)
            with open(pdfdir, "wb+") as f:
                writer.write(f)

            image.close()



            watermark_instance = PdfFileReader(pdfdir)
            watermark_page = watermark_instance.getPage(0)
            pdf_reader = PdfFileReader(f"docs/{docid}.pdf")
            pdf_writer = PdfFileWriter()
            for page in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page)
                page.mergePage(watermark_page)
                pdf_writer.addPage(page)
            with open(f"docs/retrieving/{docname}.pdf", 'wb') as out:
                pdf_writer.write(out)



            os.remove(watermarkdir)
            os.remove(pdfdir)



            await msg.edit(content=None, attachments=[discord.File(f"docs/retrieving/{docname}.pdf")])
            os.remove(f"docs/retrieving/{docname}.pdf")
        else:
            await msg.edit(content="Not cleared")
    else:
        await msg.edit(content="Document does not exist")

@client.command()
async def delete(ctx, *, docid):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["whitelist"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        docexits, creator = False, False
        with open(docs, "r+") as f:
            data = json.load(f)
            docexists = False
            if docid in data["docs"]:
                docexists = True
                if data["docs"][docid]["author"] == ctx.author.id:
                    creator = True
        if docexists == True:
            if creator == True:
                with open(docs, "r+") as f:
                    data = json.load(f)
                    data["docs"].pop(docid)
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                os.remove(f"docs/{docid}.pdf")
                await msg.edit(content="Deleted")
            else:
                await msg.edit(content="You are not the document's author")
        else:
            await msg.edit(content="Document does not exist")
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def myclearances(ctx):
    hasclearances = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if str(ctx.author.id) in data["clearances"]:
            hasclearances = True
            allclearances = []
            for el in data["clearances"][str(ctx.author.id)]:
                allclearances.append(el)
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if hasclearances == True:
        totalclearances = ""
        for el in allclearances:
            totalclearances = f"{totalclearances}{el}\n"
        totalclearances = totalclearances.rstrip("\n")
        await msg.edit(content=f"You have the following clearances:```\n{totalclearances}\n```")
    else:
        await msg.edit(content="You have no department-specific clearances")

@client.command()
async def clear(ctx, who : discord.Member, *, clearance):
    whitelisted, selfcleared = False, False
    clearance = clearance.upper()
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if str(ctx.author.id) in data["depadministration"]:
            whitelisted = True
            if clearance in data["depadministration"][str(ctx.author.id)]:
                selfcleared = True
        elif int(ctx.author.id) in data["administration"]:
            whitelisted = True
            selfcleared = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        if selfcleared == True:
            allclearances = ["WASHTOW", "FRB", "USCP", "MPD", "BUS", "BOP", "DOT", "DSS", "DOTT", "CSPAN", "DIA", "FRP", "SF", "DFPA", "FBI", "USM", "DOCAL", "USMS", "CIA", "NSA", "DCCC", "FPS", "JB", "SWAT", "SS", "DHS", "DOD", "DOS", "WHS", "DOJ", "TTS", "WF", "TAXI", "DCEMS", "DCFD"]
            if clearance in allclearances:
                with open(whitelist, "r+") as f:
                    if str(who.id) in data["clearances"]:
                        if clearance in data["clearances"][str(who.id)]:
                            await msg.edit(content=f"{who.mention} already has clearance for `{clearance}`")
                        else:
                            data["clearances"][str(who.id)].append(clearance)
                            await msg.edit(content=f"{who.mention} has been cleared for `{clearance}`")
                    else:
                        data["clearances"][str(who.id)] = [
                            clearance
                        ]
                        await msg.edit(content=f"{who.mention} has been cleared for `{clearance}`")
                    if int(who.id) not in data["whitelist"]:
                        data["whitelist"].append(int(who.id))
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
            else:
                await msg.edit(content=f"The clearance `{clearance}` does not exist")
        else:
            await msg.edit(content=f"Not a Department Administrator for `{clearance}`")
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def unclear(ctx, who : discord.Member, *, clearance):
    whitelisted, selfcleared = False, False
    clearance = clearance.upper()
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if str(ctx.author.id) in data["depadministration"]:
            whitelisted = True
            if clearance in data["depadministration"][str(ctx.author.id)]:
                selfcleared = True
        elif int(ctx.author.id) in data["administration"]:
            whitelisted = True
            selfcleared = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        if selfcleared == True:
            allclearances = ["WASHTOW", "FRB", "USCP", "MPD", "BUS", "BOP", "DOT", "DSS", "DOTT", "CSPAN", "DIA", "FRP", "SF", "DFPA", "FBI", "USM", "DOCAL", "USMS", "CIA", "NSA", "DCCC", "FPS", "JB", "SWAT", "SS", "DHS", "DOD", "DOS", "WHS", "DOJ", "TTS", "WF", "TAXI", "DCEMS", "DCFD"]
            if clearance in allclearances:
                with open(whitelist, "r+") as f:
                    if str(who.id) in data["clearances"]:
                        if clearance in data["clearances"][str(who.id)]:
                            data["clearances"][str(who.id)].remove(clearance)
                            f.seek(0)
                            f.truncate()
                            json.dump(data, f, indent=4)
                            if data["clearances"][str(who.id)] == []:
                                del data["clearances"][str(who.id)]
                                if int(who.id) in data["whitelist"]:
                                    data["whitelist"].remove(int(who.id))
                                f.seek(0)
                                f.truncate()
                                json.dump(data, f, indent=4)
                            await msg.edit(content=f"{who.mention} has had their clearance for `{clearance}` revoked")
                        else:
                            await msg.edit(content=f"{who.mention} isn't cleared for `{clearance}`")
                    else:
                        await msg.edit(content=f"{who.mention} isn't cleared for any agency")
            else:
                await msg.edit(content=f"The clearance `{clearance}` does not exist")
        else:
            await msg.edit(content=f"Not a Department Administrator for `{clearance}`")
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def mydeps(ctx):
    hasdeps = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if str(ctx.author.id) in data["depadministration"]:
            hasdeps = True
            alldeps = []
            for el in data["clearances"][str(ctx.author.id)]:
                alldeps.append(el)
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if hasdeps == True:
        totaldeps = ""
        for el in alldeps:
            totaldeps = f"{totaldeps}{el}\n"
        totaldeps = totaldeps.rstrip("\n")
        await msg.edit(content=f"You have the following clearances:```\n{totaldeps}\n```")
    else:
        await msg.edit(content="You have no department-specific clearances")

@client.command()
async def dbtest(ctx):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        with open(groups, "r+") as f:
            data = json.load(f)
            allgroups = ""
            for el in data["groups"]:
                allgroups= f"{allgroups}\n__{el}__ - {data['groups'][el]['groupid']} - {data['groups'][el]['suspendedname']}"
            allgroups = allgroups.lstrip("\n")
        embed = discord.Embed(
            title="Groups",
            colour=0x000000,
            description=allgroups
        )
        embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
        await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def clearances(ctx, *, who : discord.Member):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        hasclearances = False
        with open(whitelist, "r+") as f:
            data = json.load(f)
            if str(who.id) in data["clearances"]:
                hasclearances = True
                clearanceslist = []
                for el in data["clearances"][str(who.id)]:
                    clearanceslist.append(el)
        if hasclearances == True:
            embed = discord.Embed(
                title="Clearances",
                colour=0x000000,
                description=""
            )
            embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
            desc = f"{who.mention}**'s Clearances:**"
            for el in clearanceslist:
                desc = f"{desc}\n{el}"
            embed.description = desc
            await msg.edit(content=None, embed=embed)
        else:
            await msg.edit(content=f"{who.mention} has no clearances")
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def deps(ctx, *, who : discord.Member):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        hasclearances = False
        with open(whitelist, "r+") as f:
            data = json.load(f)
            if str(who.id) in data["depadministration"]:
                hasclearances = True
                clearanceslist = []
                for el in data["depadministration"][str(who.id)]:
                    clearanceslist.append(el)
        if hasclearances == True:
            embed = discord.Embed(
                title="Department Administrator",
                colour=0x000000,
                description=""
            )
            embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
            desc = f"{who.mention}**'s Departments:**"
            for el in clearanceslist:
                desc = f"{desc}\n{el}"
            embed.description = desc
            await msg.edit(content=None, embed=embed)
        else:
            await msg.edit(content=f"{who.mention} has no departments")
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def query(ctx, *, who : discord.Member):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        whoid = int(who.id)
        ans = False
        with open(whitelist, "r+") as f:
            data = json.load(f)
            if whoid in data["whitelist"]:
                ans = True
        embed = discord.Embed(
            title="Query",
            colour=0x000000,
            description=""
        )
        embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
        if ans == True:
            embed.description = f"{who.mention} has access to the Imperum Service."
        else:
            embed.description = f"{who.mention} does not have access to the Imperum Service."
        await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def grant(ctx, *, who : discord.Member):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        whoid = int(who.id)
        isin = False
        with open(whitelist, "r+") as f:
            data = json.load(f)
            if whoid in data["whitelist"]:
                isin = True
            else:
                data["whitelist"].append(whoid)
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
        embed = discord.Embed(
            title="Grant",
            colour=0x000000,
            description=""
        )
        embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
        if isin == True:
            embed.description = f"{who.mention} already has access to the Imperum Service."
        else:
            embed.description = f"{who.mention} has been granted access to the Imperum Service."
        await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def revoke(ctx, *, who : discord.Member):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        whoid = int(who.id)
        isin = True
        with open(whitelist, "r+") as f:
            data = json.load(f)
            if whoid in data["whitelist"]:
                data["whitelist"].remove(whoid)
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            else:
                isin = False
        embed = discord.Embed(
            title="Revoke",
            colour=0x000000,
            description=""
        )
        embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
        if isin == True:
            embed.description = f"{who.mention}'s access to the Imperum Service has been revoked."
        else:
            embed.description = f"{who.mention} does not have Imperum access, and therefore cannot be removed from access."
        await msg.edit(content=None, embed=embed)
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def dep(ctx, who : discord.Member, *, department):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        department = department.upper()
        allclearances = ["WASHTOW", "FRB", "USCP", "MPD", "BUS", "BOP", "DOT", "DSS", "DOTT", "CSPAN", "DIA", "FRP", "SF", "DFPA", "FBI", "USM", "DOCAL", "USMS", "CIA", "NSA", "DCCC", "FPS", "JB", "SWAT", "SS", "DHS", "DOD", "DOS", "WHS", "DOJ", "TTS", "WF", "TAXI", "DCEMS", "DCFD"]
        if department in allclearances:
            with open(whitelist, "r+") as f:
                data = json.load(f)
                if str(who.id) in data["depadministration"]:
                    if department in data["depadministration"][str(who.id)]:
                        await msg.edit(content=f"{who.mention} already has Department Administration access for `{department}`")
                    else:
                        data["depadministration"][str(who.id)].append(department)
                        await msg.edit(content=f"{who.mention} has been granted Department Administration access for `{department}`")
                else:
                    data["depadministration"][str(who.id)] = [
                        department
                    ]
                    await msg.edit(content=f"{who.mention} has been granted Department Administration access for `{department}`")
                if str(who.id) in data["clearances"]:
                    if department not in data["clearances"][str(who.id)]:
                        data["clearances"][str(who.id)].append(department)
                else:
                    data["clearances"][str(who.id)] = [
                        department
                    ]
                if int(who.id) not in data["whitelist"]:
                    data["whitelist"].append(int(who.id))
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
        else:
            await msg.edit(content=f"The clearance `{department}` does not exist")
    else:
        await msg.edit(content="Not whitelisted")

@client.command()
async def undep(ctx, who : discord.Member, *, department):
    whitelisted = False
    with open(whitelist, "r+") as f:
        data = json.load(f)
        if int(ctx.author.id) in data["administration"]:
            whitelisted = True
    msg = await ctx.reply("<a:loading:1011088285998776372>")
    if whitelisted == True:
        department = department.upper()
        allclearances = ["WASHTOW", "FRB", "USCP", "MPD", "BUS", "BOP", "DOT", "DSS", "DOTT", "CSPAN", "DIA", "FRP", "SF", "DFPA", "FBI", "USM", "DOCAL", "USMS", "CIA", "NSA", "DCCC", "FPS", "JB", "SWAT", "SS", "DHS", "DOD", "DOS", "WHS", "DOJ", "TTS", "WF", "TAXI", "DCEMS", "DCFD"]
        if department in allclearances:
            with open(whitelist, "r+") as f:
                data = json.load(f)
                if str(who.id) in data["depadministration"]:
                    if department in data["depadministration"][str(who.id)]:
                        data["depadministration"][str(who.id)].remove(department)
                        if data["depadministration"][str(who.id)] == []:
                            del data["depadministration"][str(who.id)]
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f, indent=4)
                        if str(who.id) in data["clearances"]:
                            if department in data["clearances"][str(who.id)]:
                                data["clearances"][str(who.id)].remove(department)
                                f.seek(0)
                                f.truncate()
                                json.dump(data, f, indent=4)
                                if data["clearances"][str(who.id)] == []:
                                    del data["clearances"][str(who.id)]
                                    data["whitelist"].remove(int(who.id))
                                    f.seek(0)
                                    f.truncate()
                                    json.dump(data, f, indent=4)
                        await msg.edit(content=f"{who.mention} no longer has Department Administration access for `{department}`")
                    else:
                        await msg.edit(content=f"{who.mention} is not a Department Administrator for `{department}`, therefore nothing has changed")
                else:
                    await msg.edit(content=f"{who.mention} is not an adminstrator for any department")
        else:
            await msg.edit(content=f"The clearance `{department}` does not exist")
    else:
        await msg.edit(content="Not whitelisted")

@client.command(aliases=["cmd", "cmds", "command", "commands"])
async def help(ctx):
    embed = discord.Embed(
        title="Help",
        colour=0x000000,
        description="__**Public**__\n`!doclas` - Get information on Imperum's DOCLAS System\n\n__**Standard Whitelist**__\n`!basic {user}` - Returns basic info on a roblox user (user, id, nick, page)\n`!employment {user}` - Returns user's current jobs and ranks in them\n`!bgc {user}` - Returns a pass or fail grade for a user\n`!bgcdetail {user}` - Returns all bgc check and their grades (pass/fail)\n`!myclearances` - Check your curreny agency clearances\n\n__**DOCLAS**__\n`!index` - Returns a list of files uploaded to Imperum's DOCLAS System within the past 7 days\n`!mydocs` - Returns a list of all of your uploaded documents and their relevant information\n`!view {id}` - View a document uploaded to Imperum's DOCLAS Database\n`!upload` - Upload a PDF File to Imperum's DOCLAS Database\n`!delete {id}` - Delete one of your documents uploaded to Imperum's DOCLAS Database\n\n__**Department Administration**__\n`!clear {user} {clearance}` - Grants the mentioned user access to the specified agency's clearance\n`!unclear {user} {clearance}` - Revokes the mentioned user's access to the specified agency's clearance\n`!mydeps` - Check which departments you have administrative control over\n\n__**Administration**__\n`!clearances {user}` - See which clearances a user has access to\n`!deps {user}` - Check the departments a user has administrator access to\n`!query {user}` - Check if the mentioned user has access to the Imperum Service\n`!grant {user}` - Grant the specified user access to the Imperum Service\n`!revoke {user}` - Remove the specified user's Imperum Service access\n`!dep {user} {deparment}` - Sets the user as a department administrator for the specified department\n`!undep {user} {department}` - Removes the user as a department adminsitrator for the specified department"
    )
    embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
    await ctx.reply(embed=embed)

@client.command()
async def doclas(ctx):
    embed = discord.Embed(
        title="DOCLAS",
        colour=0x000000,
        description="`DOCLAS` Shorthand for Document Classification is a part of the Imperum Service which enables users to upload a PDF File to the Imperum Service index which can only be viewed by users which obtain specified classifications by the author.\nWhen uploading, you will be asked to upload your file and the required clearances. The file's name will be grabbed from the uploaded filename (excluding .pdf)\nEvery document within the database has a unique ID which allows users to then `!view` the document if they have clearance, and the author can `!delete` the document if they wish to do so.\nAll clearance types:\nWASHTOW, FRB, USCP, MPD, BUS, BOP, DOT, DSS, DOTT, CSPAN, DIA, FRP, SF, DFPA, FBI, USM, DOCAL, USMS, CIA, NSA, DCCC, FPS, JB, SWAT, SS, DHS, DOD, DOS, WHS, DOJ, TTS, WF, TAXI, DCEMS, DCFD\nThe testing or abuse of this feature may result in action towards your access to the Imperum Service."
    )
    embed.set_thumbnail(url="https://i.ibb.co/ck3hmVm/Logo.png")
    await ctx.reply(embed=embed)

client.run('MTAwNjk0Mzc1NTM3MjM0MzI5Ng.GWFSgf.FKZssJEXYyr5XpmQJmGC_2ZNO3nvBw62vNWNO8')