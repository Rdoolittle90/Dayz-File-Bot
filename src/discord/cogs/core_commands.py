import datetime
from nextcord.ext import commands
import nextcord
from src.helpers.colored_logging import colorize_log
from src.discord.modals.announcement_creator import AnnouncementCreator
from src.discord.guild_manager import set_announce_channel
from src.discord.bot import DiscordBot



class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Core Cog"
        colorize_log("INFO", f"{self.name} Connected")


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="set_announcement_channel", description="Set the bot's announcement channel")
    async def set_announcement_channel(self, interaction: nextcord.Interaction, channel_id: str):
        colorize_log("INFO", f"{interaction.user.name} used CoreCog.set_announcement_channel at {datetime.datetime.now()}")
        """Sets the bot's announcement channel to the given channel ID."""
        await interaction.response.defer(ephemeral=True)
        channel = await set_announce_channel(interaction.guild, int(channel_id))
        await interaction.followup.send(channel)


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="make_announcement", description="send an announcement to the set channel or preview in this channel.")
    async def make_announcement(self, interaction: nextcord.Interaction, preview:int=0):
        colorize_log("INFO", f"{interaction.user.name} used CoreCog.make_announcement at {datetime.datetime.now()}")
        """make an announcement"""
        await interaction.response.send_modal(modal=AnnouncementCreator(self.bot, preview))


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def bot_shutdown(self, interaction: nextcord.Interaction) -> None:
        colorize_log("WARNING", f"{interaction.user.name} used CoreCog.kill at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()


def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))