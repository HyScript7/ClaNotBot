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
token = str(config("TOKEN"))

# This is the custom bot class, which we made by inheriting from discord's Client
class appclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = GUILDID)
            self.synced = True
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

"""
Example return from the API call:
{1: {'subject': 'Fyzika', 'teacher': 'Mgr. Pavla Bělašková'}, 2: {'subject': 'Matematika', 'teacher': 'Mgr. Pavla Bělašková'}, 3: {'subject': 'Anglický jazyk', 'teacher': 'Jaromír Kastner'}, 4: {'subject': 'Operační systémy', 'teacher': 'Ing Jaroslav Burda Bc'}, 5: {'subject': 'Anglický jazyk', 'teacher': 'Mgr. Marija Vlčková'}, 6: {'subject': '', 'teacher': ''}}
"""

@tree.command(name = "schedule", description="Sends today's time schedule", guild=GUILDID)
async def _schedule(interaction: discord.Interaction):
    Class = "1.I" #TODO: Make this be fetched automaticaly in the API Wrapper
    Group = "Placeholder" #TODO: Make some student group resolution in the wrapper for the API wrapper.
    # Set the current week and day
    week = "YYYY-MM-DD"
    day = 1 # 1 - 5 (Mo - Fr)
    e = discord.Embed(colour=discord.Colour(int('006B76', 16)),
                      timestamp=time.time())
    e.author = f"(ClaNot) {Class}  {Group}"
    timeschedule = baka.GetTimetable("https://sbakalari.gasos-ro.cz", bakauser, bakapass, week, day)
    for i in timeschedule:
        e.add_field(timeschedule[i]["subject"], f"{timeschedule[i]['room']} **{timeschedule[i]['teacher']}**")
    await interaction.response.send_message(embed=e)

# Run the bot
client.run(token)
