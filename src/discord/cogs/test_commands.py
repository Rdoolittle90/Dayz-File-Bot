import asyncio
import datetime
from nextcord.ext import commands
import nextcord
from src.helpers.colored_printing import colorized_print

from src.discord.bot import DiscordBot


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Testing"
        colorized_print("COG", self.name)

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="debug_atm_get_all", description="placeholder description 1")
    async def debug_atm_get_all(self, interaction: nextcord.Interaction):
        colorized_print("WARNING", f"{interaction.user.name} used TestingCog.debug_atm_get_all at {datetime.datetime.now()}")
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
        colorized_print("WARNING", f"{interaction.user.name} used TestingCog.get_server_status at {datetime.datetime.now()}")
        """placeholder method"""
        utc_now = datetime.datetime.utcnow()
        now = datetime.datetime.now()

        time_diff = utc_now - self.bot.cftools.utc_then

        if time_diff >= datetime.timedelta(seconds=30) or self.bot.cftools.server_info[0] == {}:
            self.utc_last = datetime.datetime.utcnow()
            for idx, server_map in enumerate(self.bot.cftools.map_info.keys()):
                server_id = self.bot.cftools.map_info[server_map]["map_id"]
                response = self.bot.cftools.make_authenticated_request("GET", f"https://data.cftools.cloud/v1/gameserver/{server_id}", token=self.bot.cftools.token)
                data = response.json()
                name = data[server_id]['name'].split(" ")[1].title()
                self.bot.cftools.server_info[idx]["name"] = name
                self.bot.cftools.server_info[idx]["status"] = "Online" if data[server_id]['online'] else "Offline"
                self.bot.cftools.server_info[idx]["players"] = data[server_id]['status']['players']
                self.bot.cftools.server_info[idx]["slots"] = data[server_id]['status']['slots']


        server_status_list = [
            self.bot.cftools.server_info[0]["status"], 
            self.bot.cftools.server_info[1]["status"], 
            self.bot.cftools.server_info[2]["status"]
        ]
        
        color, status_emoji = format_status(server_status_list)
        # Create a new embed
        embed = nextcord.Embed(title="Platinum Server Status", color=color, timestamp=now)

        # Add fields to the embed
        for idx in range(0, 3):
            name = self.bot.cftools.server_info[idx]["name"]
            status = self.bot.cftools.server_info[idx]["status"]
            players = self.bot.cftools.server_info[idx]["players"]
            slots = self.bot.cftools.server_info[idx]["slots"]

            embed.add_field(
                name=f'[#{idx+1}] {name}', 
                value=f'{status_emoji}: `{status}`\nPlayers: `{players}/{slots}`', 
                inline=True
                )

        # Send the embed to a channel
        await interaction.channel.send(embed=embed)

    


def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))
    


def format_status(server_status_list: list[bool]) -> tuple[nextcord.Color, str]:
    """
    Given a list of 3 booleans representing server statuses, returns a tuple containing a color and a status emoji.

    Args:
    - server_status_list (list[bool]): A list of 3 booleans representing server statuses, where True means the server is online and False means it is offline.

    Returns:
    - A tuple containing a `nextcord.Color` object and a string representing a status emoji.
    """
    if all(server_status_list):
        # If all servers are online, set the color to green and the emoji to a green circle.
        color = nextcord.Color.green()
        status_emoji = "🟢"
    elif not any(server_status_list):
        # If all servers are offline, set the color to red and the emoji to a red circle.
        color = nextcord.Color.red()
        status_emoji = "🔴"
    else:
        # Otherwise, set the color to orange and the emoji to an orange circle.
        color = nextcord.Color.orange()
        status_emoji = "🟠"

    # Return a tuple containing the color and status emoji.
    return color, status_emoji

