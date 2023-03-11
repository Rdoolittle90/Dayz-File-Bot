import datetime
import inspect
from nextcord.ext import commands
import nextcord
from src.discord.embeds.leaderboard import every_map_leaderboard_embed, single_map_leaderboard_embed
from src.discord.embeds.server_status import server_status_embed
from src.helpers.colored_printing import colorized_print
from src.discord.embeds.player_profile import create_profile_card_embed
from src.discord.modals.registration import EnterSteamID
from src.discord.bot import DiscordBot



class DayzUserCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "DayZ User"

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="register your steam 64 ID")
    async def register(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """placeholder"""
        await interaction.response.send_modal(modal=EnterSteamID(self.bot))


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="profile", description="View your player card")
    async def profile(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """placeholder"""
        await interaction.channel.send(embed=await create_profile_card_embed(self.bot, interaction.user.id))


    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="server_status", description="placeholder description 1")
    async def server_status(self, interaction: nextcord.Interaction):
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """placeholder method"""
        await interaction.response.defer(ephemeral=False)
        # Send the embed to a channel
        await interaction.followup.send(embed=server_status_embed(self.bot))


   # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_leaderboard", description="placeholder description 1")
    async def get_leaderboard(self, interaction: nextcord.Interaction, map_name:str=None):
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer(ephemeral=False)
        self.bot.cftools.get_leaderboard_info()
        if map_name:
            leaderboards = self.bot.cftools.read_leaderboard_info(map_name, limit=100)
            await interaction.followup.send(embed=single_map_leaderboard_embed(map_name, leaderboards[map_name]))
            colorized_print("DEBUG", f"single_map_leaderboard sent to channel {interaction.channel}")
        else:
            leaderboards = self.bot.cftools.read_leaderboard_info(limit=100)
            await interaction.followup.send(embed=every_map_leaderboard_embed(leaderboards))
            colorized_print("DEBUG", f"every_map_leaderboard sent to channel {interaction.channel}")


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="atm", description="View your ATMs")
    async def atm(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="inventory", description="View your discord item inventory")
    async def inventory(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="trade", description="Trade Discord Stashed items")
    async def trade(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DayzUserCog(bot))