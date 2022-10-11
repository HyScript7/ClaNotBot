import discord
from discord import app_commands
from decouple import config
import time
import datetime
from clanot import bakapiwrap as baka
from clanot import bakapi # Rewrite wrapper using classes and async functions

GUILDID = discord.Object(id=1019661946590609538)

# Set tokens and stuff from a .env file
bakauser = str(config("BAKAUSER"))
bakapass = str(config("BAKAPASS"))
#TODO: Change token and baka auth to use the rewrite token class
bakatoken = None # If type of bakatoken is None, it means we haven't been given a login token yet.
bakarefresh = None
bakatime = 0 # Keeps track of when the token was last updated.
bakamaxtime = 300 # 5 Minutes before needing re-auth
token = str(config("TOKEN")) # Bot token

#TODO: Remove this function once bakapi is rewritten, as this will be handled within the token class function
async def bapitok():
    global bakatoken, bakarefresh, bakatime
    if round(time.time())-bakatime <= bakamaxtime:
        return
    if bakarefresh is None:
        x = baka.Login("https://sbakalari.gasos-ro.cz", bakauser, bakapass)
    else:
        x = baka.Refresh("https://sbakalari.gasos-ro.cz", bakarefresh)
    bakatime = round(time.time())
    bakatoken = x.get("token")
    bakarefresh = x.get("refresh")

async def parseDate(stamp: int):
    #TODO: Actually parse the date from the timestamp
    year = "2022"
    month = "01"
    day = "01"
    weekdaynum = 1 # Monday
    return (f"{year}, {month}, {day}", weekdaynum)

class appclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        global bakatoken
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = GUILDID)
            self.synced = True
        await bapitok()
        print(f"Logged into Bakalari using the username {bakauser} - Token and Password Hidden, use debugger to view in variables")
        print(f"We have logged in as {self.user}.")

# Define our client/bot
client = appclient()
tree = app_commands.CommandTree(client)

"""
# Command Template
@tree.command(name = "test", description = "testing", guild=GUILDID)
async def _test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}!\nIt is {time.getDate(round(time.time()))}")
"""

@tree.command(name = "schedule", description="Sends today's time schedule", guild=GUILDID)
async def _schedule(interaction: discord.Interaction):
    # Set the current week and day
    week, day = await parseDate(time.time())
    e = discord.Embed(colour=discord.Colour(int('5555FF', 16)))
    await bapitok()
    timeschedule = baka.GetTimetable(baka.GetRawTimetable("https://sbakalari.gasos-ro.cz", bakatoken, week), week, day)
    for y, i in enumerate(timeschedule):
        e.add_field(name=f'{y+1}. {timeschedule[i]["subject"]}', value=f"Učebna {timeschedule[i]['room']}\n{timeschedule[i]['teacher']}")
    await interaction.response.send_message(embed=e)

# Run the bot
client.run(token)
