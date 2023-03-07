from nextcord.ext import commands
import nextcord
from src.helpers.colored_logging import colorize_log
from src.discord.bot import DiscordBot


class AdminCog(commands.Cog):
    # =====================================================================================================
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Admin Cog"
        colorize_log("INFO", "{:<16} Connected".format(self.name))


def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))