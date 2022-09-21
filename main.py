import discord
from discord import app_commands
from decouple import config
import time
import datetime
from clanot import bakapiwrap as baka

# The Guild ID on Discord for which we are configuring the bot to run on.
GUILDID = discord.Object(id = 1019661946590609538)

bakauser = str(config("BAKAUSER"))
bakapass = str(config("BAKAPASS"))
bakatoken = None # If type of bakatoken is None, it means we haven't been given a login token yet.
bakarefresh = None
bakatime = 0 # Keeps track of when the token was last updated.
bakamaxtime = 300 # How often in seconds should we refresh the token (extend)  
bottoken = str(config("TOKEN"))

#! Requires testing
async def bapitok():
    global bakatoken, bakarefresh, bakatime
    if round(time.time())-bakatime < bakamaxtime:
        return
    if type(bakarefresh) is None:
        x = baka.Login("https://sbakalari.gasos-ro.cz", bakauser, bakapass)
    else:
        x = baka.RefreshToken("https://sbakalari.gasos-ro.cz", bakarefresh)
    bakatime = round(time.time())
    bakatoken = x.get("token")
    bakarefresh = x.get("refresh")

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

client = appclient()
tree = app_commands.CommandTree(client)

"""
# Command Template
@tree.command(name = "test", description = "testing", guild =GUILDID)
async def _test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}!\nIt is {time.getDate(round(time.time()))}")
"""

@tree.command(name = "schedule", description="Sends today's time schedule", guild =GUILDID)
async def schedule(interaction: discord.Interaction):
    await bapitok()
    Class = "1.I" #TODO: API Wrapper function to fetch class name
    Group = "Placeholder" #TODO: API Wrapper function to fetch student's group 

    week = "2022-09-19" # YYYY-MM-DD - If the day or month are single digit, a zero has to be added before the day. Eg: 2nd of January would be 2022-01-02
    day = 1 # 1 - 5 (Mo - Fr)
    #TODO: Return and send a no classes message if it's a weekend
    if False:
        pass
    # Fetch the time table
    timeschedule = baka.GetTimetable(baka.GetRawTimetable("https://sbakalari.gasos-ro.cz", bakatoken, week), week, day)
    # Pack everything into an embed
    e = discord.Embed(colour=discord.Colour(int('006B76', 16)),
                      timestamp=time.time())
    e.author = f"(ClaNot) {Class}  {Group}"
    for i in timeschedule:
        e.add_field(timeschedule[i]["subject"], f"**{timeschedule[i]['room']}** {timeschedule[i]['teacher']}")
    await interaction.response.send_message(embed=e)

# Run the bot
client.run(bottoken)
