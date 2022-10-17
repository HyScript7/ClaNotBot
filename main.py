#        _                   _   
#    ___| | __ _ _ __   ___ | |_ 
#   / __| |/ _` | '_ \ / _ \| __|
#  | (__| | (_| | | | | (_) | |_ 
#   \___|_|\__,_|_| |_|\___/ \__|
#
# Version: 2.1
# Authors: HyScript7, Mobilex
# License: MIT License
# Copyright (c) 2022 HyScript7 & mobilex1122
#
import discord
from discord import app_commands
from decouple import config
import time
import random
from clanot import bakapiwrap as baka
from clanot import bakapi # API Wrapper rewrite with classes and async functions.
from clanot import icanteenwrap as icanapi # iCanteen API Wrapper

GUILDID = discord.Object(id=1019661946590609538)

token = str(config("TOKEN")) # Discord Bot Token
bakapiurl = "https://sbakalari.gasos-ro.cz" # Bakaláři URL to use with our wrapper
icanapiurl = "" # iCanteen URL - Might not work for all sites, and mofications to the wrapper might have to be made, depending on the site setup/theme.

seconds_day = 24*60*60
seconds_week = 7*seconds_day


async def getRandomColor(seed: int):
    """
    Function used to generate pseudo-random embed colors.
    """
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
            # We get the envrionment variables for Bakláři authentication. Users will be able to authenticate using their own account in the future. There is also no reason to keep the authentication details in the global scope.
            bakauser = str(config("BAKAUSER"))
            bakapass = str(config("BAKAPASS"))
            self.bakaToken = bakapi.token(bakapiurl, bakauser, bakapass)

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
        client.timeSchedules[week] = bakapi.timetable(bakapiurl)
    raw = await client.timeSchedules[week].fetchTimetable(client.bakaToken, week)
    # timeschedule = baka.GetTimetable(raw, week, day)
    timeschedule = await client.timeSchedules[week].parseTimetable(raw, day)
    # Create embed
    dayname = ["None", "Monday", "Tuesday", "Wednessday", "Thurstday", "Friday", "Saturday", "Sunday"]
    rcolor = await getRandomColor(day)
    e = discord.Embed(colour=discord.Colour(int(rcolor, 16)), title=f"Timetable {week.replace(', ', '/')} {dayname[day]}")
    for y, i in enumerate(timeschedule):
        e.add_field(name=f'{y+1}. {i["subject"]}', value=f"Učebna {i['room']}\n{i['teacher']}")
    await interaction.response.send_message(embed=e)

@tree.command(name = "fullschedule", description="Sends today's time schedule", guild=GUILDID)
async def _week(interaction: discord.Interaction):
    # Set the current week and day
    week, day = await bakapi.timetable.parseFromTimestamp(bakapi.timetable, time=time.time())
    day +=  1
    # Get schedule
    if not week in client.timeSchedules:
        client.timeSchedules[week] = bakapi.timetable(bakapiurl)
    raw = await client.timeSchedules[week].fetchTimetable(client.bakaToken, week)
    dayname = ["None", "Monday (Pondělí)", "Tuesday (Úterý)", "Wednesday (Středa)", "Thursday (Čtvrtek)", "Friday (Pátek)", "Saturday (Sobota)", "Sunday (Neděle)"]
    elist = []
    for day in range(1,6):
        #timeschedule = baka.GetTimetable(raw, week, day)
        timeschedule = await client.timeSchedules[week].parseTimetable(raw, day)
        rcolor = await getRandomColor(day)
        e = discord.Embed(colour=discord.Colour(int(str(rcolor), 16)), title=f"Timetable {week.replace(', ', '/')} {dayname[day]}")
        for y, i in enumerate(timeschedule):
            e.add_field(name=f'{y+1}. {i["subject"]}', value=f"Učebna {i['room']}\n{i['teacher']}")
        elist.append(e)
    await interaction.response.send_message(embeds=elist)

# Run the bot
client.run(token)
