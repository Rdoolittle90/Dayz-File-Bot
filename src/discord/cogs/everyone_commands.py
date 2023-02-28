from nextcord.ext import commands
import nextcord
from discord.bot import DiscordBot

from src.discord.modals.registration import EnterSteamID



class EveryoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Everyone Cog Connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="placeholder description 1")
    async def register(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        await interaction.response.send_modal(modal=EnterSteamID(self.bot))


    # =====================================================================================================
    # @nextcord.slash_command(dm_permission=False, name="placeholder", description="placeholder description 1")
    # async def placeholder(self, interaction: nextcord.Interaction):
    #     """placeholder method"""
    #     pass


def setup(bot: commands.Bot):
    bot.add_cog(EveryoneCog(bot))