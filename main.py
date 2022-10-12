import discord
from discord import app_commands
from decouple import config
import time
import random
from clanot import bakapiwrap as baka
from clanot import bakapi # API Wrapper rewrite with classes and async functions.

GUILDID = discord.Object(id=1019661946590609538)

# Set tokens and stuff from a .env file
bakauser = str(config("BAKAUSER"))
bakapass = str(config("BAKAPASS"))
token = str(config("TOKEN")) # Discord Bot Token
apiurl = "https://sbakalari.gasos-ro.cz"

async def getRandomColor(seed: int):
    random.seed(seed**seed)
    color = random.randint(0,16777215)
    color = format(color,'x')
    return color

class appclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.bakaToken = None
        self.timeSchedules = {}
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = GUILDID)
            self.synced = True
            print("Commands synced!")
        if self.bakaToken is None:
            self.bakaToken = bakapi.token(apiurl, bakauser, bakapass)

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
async def _day(interaction: discord.Interaction):
    # Set the current week and day
    week, day = await bakapi.timetable.parseFromTimestamp(bakapi.timetable, time=time.time())
    day +=  1
    # Get schedule
    if not week in client.timeSchedules:
        client.timeSchedules[week] = bakapi.timetable(apiurl)
    raw = await client.timeSchedules[week].fetchRawWeek(client.bakaToken, week)
    timeschedule = baka.GetTimetable(raw, week, day)
    # Create embed
    dayname = ["None", "Monday", "Tuesday", "Wednessday", "Thurstday", "Friday", "Saturday", "Sunday"]
    rcolor = await getRandomColor(day)
    e = discord.Embed(colour=discord.Colour(int(rcolor, 16)), title=f"Timetable {week.replace(', ', '/')} {dayname[day]}")
    for y, i in enumerate(timeschedule):
        e.add_field(name=f'{y+1}. {timeschedule[i]["subject"]}', value=f"Učebna {timeschedule[i]['room']}\n{timeschedule[i]['teacher']}")
    await interaction.response.send_message(embed=e)

@tree.command(name = "fullschedule", description="Sends today's time schedule", guild=GUILDID)
async def _week(interaction: discord.Interaction):
    # Set the current week and day
    week, day = await bakapi.timetable.parseFromTimestamp(bakapi.timetable, time=time.time())
    day +=  1
    # Get schedule
    if not week in client.timeSchedules:
        client.timeSchedules[week] = bakapi.timetable(apiurl)
    raw = await client.timeSchedules[week].fetchRawWeek(client.bakaToken, week)
    dayname = ["None", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    elist = []
    for day in range(1,6):
        timeschedule = baka.GetTimetable(raw, week, day)
        rcolor = await getRandomColor(day)
        e = discord.Embed(colour=discord.Colour(int(str(rcolor), 16)), title=f"Timetable {week.replace(', ', '/')} {dayname[day]}")
        for y, i in enumerate(timeschedule):
            e.add_field(name=f'{y+1}. {timeschedule[i]["subject"]}', value=f"Učebna {timeschedule[i]['room']}\n{timeschedule[i]['teacher']}")
        elist.append(e)
    await interaction.response.send_message(embeds=elist)

# Run the bot
client.run(token)
