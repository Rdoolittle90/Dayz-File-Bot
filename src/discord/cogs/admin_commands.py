from nextcord.ext import commands
import nextcord
from src.discord.bot import DiscordBot


class AdminCog(commands.Cog):
    # =====================================================================================================
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Admin Cog Connected")


def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))