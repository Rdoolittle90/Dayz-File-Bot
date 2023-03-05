import asyncio
import datetime
import hashlib
from os import getenv
from nextcord.ext import commands
import nextcord
import requests

from src.discord.bot import DiscordBot


def generate_server_id(game_identifier: int, ipv4: str, game_port: int) -> str:
    # Build the string using the given parameters
    server_string = f"{game_identifier}{ipv4}{game_port}"
    
    # Hash the string using SHA-1
    hash_object = hashlib.sha1(server_string.encode())
    
    # Get the hex digest of the hash
    hex_digest = hash_object.hexdigest()
    
    # Return the hex digest as the server ID
    return hex_digest


def make_authenticated_request(method, url, token=None, json=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.request(method, url, headers=headers, json=json)
    if response.status_code == 401 and response.json().get("error") == "expired-token":
        # Token has expired, reauthenticate
        token = authenticate()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.request(method, url, headers=headers, json=json)
        response.raise_for_status()

    return response


def authenticate():
    auth_url = "https://data.cftools.cloud/v1/auth/register"
    payload = {"application_id": getenv("CFTools_App_ID"), "secret": getenv("CFTools_secret")}
    response = requests.post(auth_url, json=payload)
    response.raise_for_status()
    return response.json()["token"]

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
            response = make_authenticated_request("GET", f"https://data.cftools.cloud/v1/gameserver/{server_map}", token=self.bot.cftools_token)
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


