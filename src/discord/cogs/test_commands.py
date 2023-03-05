import asyncio
from nextcord.ext import commands
import nextcord

from src.discord.bot import DiscordBot
from tester import make_authenticated_request


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("!!! Testing Cog Connected !!!")

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
    @nextcord.slash_command(dm_permission=False, name="debug_atm_get_all", description="placeholder description 1")
    async def get_server_status(self, interaction: nextcord.Interaction):
        """placeholder method"""# Access the specific data you want to include in the embed

        response = make_authenticated_request("GET", f"https://data.cftools.cloud/v1/gameserver/4a1c3f05ef5f6f7004286b8c8f73ef1061e54e1a", token=TOKEN, json=lb_payload)
        data = response.json()
        server_name = data['4a1c3f05ef5f6f7004286b8c8f73ef1061e54e1a']['name']
        server_status = data['4a1c3f05ef5f6f7004286b8c8f73ef1061e54e1a']['status']['online']
        server_players = data['4a1c3f05ef5f6f7004286b8c8f73ef1061e54e1a']['status']['players']
        server_slots = data['4a1c3f05ef5f6f7004286b8c8f73ef1061e54e1a']['status']['slots']
        server_mods = "\n".join([f"- {mod['name']} (file ID: {mod['file_id']})" for mod in data['4a1c3f05ef5f6f7004286b8c8f73ef1061e54e1a']['mods']])

        # Create a new embed
        embed = nextcord.Embed(title=server_name, color=0x00ff00)

        # Add fields to the embed
        embed.add_field(name="Status", value="Online" if server_status else "Offline", inline=True)
        embed.add_field(name="Players", value=f"{server_players}/{server_slots}", inline=True)
        embed.add_field(name="Mods", value=server_mods, inline=False)

        # Send the embed to a channel
        await interaction.channel.send(embed=embed)

    


def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))


