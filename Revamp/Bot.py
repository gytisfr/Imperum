import discord, requests, json
from discord.ext import commands
from discord import app_commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command("help")
tree = client.tree

groupids = [758071, 15052264, 14452083, 15052318, 14451066, 761706, 5704866, 15052331, 32902509, 2582797, 14760448, 16367093, 14451648, 761141, 14451271, 15052276, 11516976]
#Main, BCSO, BCTS, CPD, DPD, FBI, FLETC, BCFD, StateGov, Judiciary, USM/CNG, PDS, Parks, SS, BCSP, Moderation, QA

async def getuser(interaction, user):
    print(user)
    uid = json.loads(requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [user], "excludeBannedUsers": False}).text)
    print(uid)
    if "data" in uid:
        return uid["data"][0]
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Title", colour=0x000000, description="descstuff"), ephemeral=True)
        return False

@client.event
async def on_ready():
    print(f"Imperum now online with {round(client.latency * 1000)}ms ping.")

@tree.command(name="employment", description="List a user's jobs and positions")
async def employment(interaction : discord.Interaction, user : str):
    user = await getuser(interaction, user)
    if not user:
        return
    info = json.loads(requests.get(f"https://groups.roblox.com/v2/users/{user['id']}/groups/roles").text)
    groupranks = {el["group"]["name"]: el["role"]["name"] for el in info["data"] if el["group"]["id"] in groupids}
    embed = discord.Embed(
        title=f"{user['name']}'s Positions",
        colour=0x000000,
        description=""
    )
    if not groupranks:
        embed.description = "N/A"
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    for el in groupranks:
        embed.add_field(name=el, value=groupranks[el], inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.command()
async def connect(ctx):
    await tree.sync()

client.run("MTAwNjk0Mzc1NTM3MjM0MzI5Ng.GWFSgf.FKZssJEXYyr5XpmQJmGC_2ZNO3nvBw62vNWNO8")