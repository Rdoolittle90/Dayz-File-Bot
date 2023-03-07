from nextcord.ext import commands
import nextcord
from src.helpers.colored_logging import colorize_log
from src.discord.bot import DiscordBot



class EveryoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Everyone Cog"
        colorize_log("INFO", "{:<16} Connected".format(self.name))


    # =====================================================================================================
    # @nextcord.slash_command(dm_permission=False, name="placeholder", description="placeholder description 1")
    # async def placeholder(self, interaction: nextcord.Interaction):
    #     """placeholder method"""
    #     pass


def setup(bot: commands.Bot):
    bot.add_cog(EveryoneCog(bot))