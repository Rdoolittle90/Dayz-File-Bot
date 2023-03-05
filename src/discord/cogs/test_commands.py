import asyncio
import datetime
import hashlib
from os import getenv
from nextcord.ext import commands
import nextcord
import requests

from src.discord.bot import DiscordBot


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("!!! Testing Cog Connected !!!")

        self.server_info = {0:{}, 1:{}, 2:{}}
        self.chernarus = getenv("CFTtools_Map_1")
        self.takistan = getenv("CFTtools_Map_2")
        self.namalsk = getenv("CFTtools_Map_3")
        self.maps = [self.chernarus, self.takistan, self.namalsk]

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="debug_atm_get_all", description="placeholder description 1")
    async def debug_atm_get_all(self, interaction: nextcord.Interaction):
        """placeholder method"""
        tasks = [
            asyncio.create_task(self.bot.ftp.get_all_player_atm("Chernarus")),
            asyncio.create_task(self.bot.ftp.get_all_player_atm("Takistan")),
            asyncio.create_task(self.bot.ftp.get_all_player_atm("Namalsk")),
            asyncio.create_task(self.bot.ftp.get_all_player_atm("TestServer"))
        ]
        await asyncio.wait(tasks)


    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_server_status", description="placeholder description 1")
    async def get_server_status(self, interaction: nextcord.Interaction):
        """placeholder method"""
        await interaction.response.defer(ephemeral=False)
        for idx, server_map in enumerate(self.maps):
            response = self.bot.make_authenticated_request("GET", f"https://data.cftools.cloud/v1/gameserver/{server_map}", token=self.bot.cftools_token)
            data = response.json()
            name = data[server_map]['name'].split(" ")[1].title()
            self.server_info[idx]["name"] = name
            self.server_info[idx]["status"] = data[server_map]['online']
            self.server_info[idx]["players"] = data[server_map]['status']['players']
            self.server_info[idx]["slots"] = data[server_map]['status']['slots']


        server_status = [self.server_info[0]["status"], self.server_info[1]["status"]], self.server_info[2]["status"]
        if False not in server_status:
            color = nextcord.Color.green()
            status_emoji = "🟢"
        elif False in server_status and True in server_status:
            color = nextcord.Color.orange()
            status_emoji = "🟠"
        else:
            color = nextcord.Color.red()
            status_emoji = "🔴"
        # Create a new embed
        embed = nextcord.Embed(title="Platinum Server Status", color=color, timestamp=datetime.datetime.utcnow())

        # Add fields to the embed
        for i in range(0, 3):
            status = "Online" if self.server_info[i]["status"] else "Offline"
            embed.add_field(name=f'[#{i}] {self.server_info[i]["name"]}', value=f'{status_emoji}: `{status}`\nPlayers: `{self.server_info[i]["players"]}/{self.server_info[i]["slots"]}`', inline=True)

        # Send the embed to a channel
        await interaction.followup.send(embed=embed)

    


def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))


