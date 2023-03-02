from nextcord.ext import commands
import nextcord
from src.discord.modals.announcement_creator import AnnouncementCreator
from src.discord.guild_manager import set_announce_channel
from src.discord.bot import DiscordBot



class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Core Cog Connected")


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="set_announcement_channel", description="Set the bot's announcement channel")
    async def set_announcement_channel(self, interaction: nextcord.Interaction, channel_id: str):
        """Sets the bot's announcement channel to the given channel ID."""
        await interaction.response.defer(ephemeral=True)
        channel = await set_announce_channel(interaction.guild, int(channel_id))
        await interaction.followup.send(channel)


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="make_announcement", description="send an announcement to the set channel or preview in this channel.")
    async def make_announcement(self, interaction: nextcord.Interaction, num_fields:int=0, preview:int=0):
        """make an announcement"""
        await interaction.response.send_modal(modal=AnnouncementCreator(self.bot, num_fields, preview))


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def kill(self, interaction: nextcord.Interaction) -> None:
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()


def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))