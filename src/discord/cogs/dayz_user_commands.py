from nextcord.ext import commands
import nextcord
from src.discord.modals.registration import EnterSteamID
from src.discord.bot import DiscordBot



class DayzUserCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Dayz User Cog Connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="placeholder description 1")
    async def register(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        await interaction.response.send_modal(modal=EnterSteamID(self.bot))

    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="atm", description="placeholder description 1")
    async def atm(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="inventory", description="placeholder description 1")
    async def inventory(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="trade", description="placeholder description 1")
    async def trade(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        pass


def setup(bot: commands.Bot):
    bot.add_cog(DayzUserCog(bot))