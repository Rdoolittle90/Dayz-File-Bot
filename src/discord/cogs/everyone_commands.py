from nextcord.ext import commands
import nextcord
from src.discord.bot import DiscordBot



class EveryoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Everyone Cog Connected")


    # =====================================================================================================
    # @nextcord.slash_command(dm_permission=False, name="placeholder", description="placeholder description 1")
    # async def placeholder(self, interaction: nextcord.Interaction):
    #     """placeholder method"""
    #     pass


def setup(bot: commands.Bot):
    bot.add_cog(EveryoneCog(bot))