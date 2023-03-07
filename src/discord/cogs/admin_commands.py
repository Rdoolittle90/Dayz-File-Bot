from nextcord.ext import commands
import nextcord
from src.helpers.colored_printing import colorized_print
from src.discord.bot import DiscordBot


class AdminCog(commands.Cog):
    # =====================================================================================================
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Admin"
        colorized_print("COG", self.name)


def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))