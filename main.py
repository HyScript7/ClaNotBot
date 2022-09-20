import discord
from discord import app_commands
from decouple import config
import time
import datetime
from clanot import bakapiwrap as baka

GUILDID = 856229875824066630

# Set tokens and stuff from a .env file
bakauser = str(config("BAKAUSER"))
bakapass = str(config("BAKAPASS"))
bakatoken = None # If type of bakatoken is None, it means we haven't been given a login token yet.
bakarefresh = None
bakatime = 0 # Keeps track of when the token was last updated.
bakamaxtime = 300 # 5 Minutes before needing re-auth
token = str(config("TOKEN")) # Bot token

#TODO: Refresh instead of relogging if it expires!!!
async def bapitok():
    global bakatoken, bakarefresh, bakatime
    if round(time.time())-bakatime <= bakamaxtime:
        return
    if type(bakarefresh) is None:
        x = baka.Login("https://sbakalari.gasos-ro.cz", bakauser, bakapass)
    else:
        x = baka.Refresh("https://sbakalari.gasos-ro.cz", bakarefresh)
    bakatime = round(time.time())
    bakatoken = x.get("token")
    bakarefresh = x.get("refresh")

# This is the custom bot class, which we made by inheriting from discord's Client
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
        bakatoken = baka.login(bakauser, bakapass)
        print(f"Logged into Bakalari using the username {bakauser} - Token and Password Hidden, use debugger to view in variables")
        print(f"We have logged in as {self.user}.")

# Define our client/bot
client = appclient()
tree = app_commands.CommandTree(client) # the tree is the list of slash commands our bot has

"""
# Command Template
@tree.command(name = "test", description = "testing", guild=GUILDID)
async def _test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}!\nIt is {time.getDate(round(time.time()))}")
"""

@tree.command(name = "schedule", description="Sends today's time schedule", guild=GUILDID)
async def _schedule(interaction: discord.Interaction):
    Class = "1.I" #TODO: Make this be fetched automaticaly in the API Wrapper
    Group = "Placeholder" #TODO: Make some student group resolution in the wrapper for the API wrapper.
    # Set the current week and day
    week = "2022-09-20"
    day = 2 # 1 - 5 (Mo - Fr)
    e = discord.Embed(colour=discord.Colour(int('006B76', 16)),
                      timestamp=time.time())
    e.author = f"(ClaNot) {Class}  {Group}"
    #! Update function call, get tokens on init
    timeschedule = baka.GetTimetable("https://sbakalari.gasos-ro.cz", bakauser, bakapass, week, day)
    for i in timeschedule:
        e.add_field(timeschedule[i]["subject"], f"{timeschedule[i]['room']} **{timeschedule[i]['teacher']}**")
    await interaction.response.send_message(embed=e)

# Run the bot
client.run(token)
