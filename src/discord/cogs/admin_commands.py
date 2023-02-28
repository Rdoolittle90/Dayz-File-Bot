from nextcord.ext import commands
import nextcord
from src.discord.bot import DiscordBot

from src.discord.announcements import announce_status
from src.discord.guild_manager import set_announce_channel


class AdminCog(commands.Cog):
    # =====================================================================================================
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Admin Cog Connected")


def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))