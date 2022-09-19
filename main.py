import discord
from discord import app_commands
from decouple import config
from clanot import bakapiwrap as baka

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

client = appclient()
tree = app_commands.CommandTree(client)

"""
# Command Template
@tree.command(name = "test", description = "testing", guild=GUILDID)
async def _test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}!\nIt is {time.getDate(round(time.time()))}")
"""
