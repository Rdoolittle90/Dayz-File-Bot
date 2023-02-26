from nextcord.ext import commands
import nextcord

from src.discord.announcements import announce_status
from src.discord.guild_manager import get_map_selections, set_announce_channel
from src.discord.load_traderconfig import load_traderconfig_view
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.file_manager import create_new_map_dir, get_map_key, key_embed


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin Cog Connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="set_status", description="placeholder description")
    async def set_status(self, interaction: nextcord.Interaction, status_code: int, map_name: str = "ALL", message: str = None):
        """status_codes: 0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
        await announce_status(interaction, status_code, map_name, message)

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="set_announcement_channel", description="placeholder description")
    async def set_announcement_channel(self, interaction: nextcord.Interaction, channel_id: str):
        """sets the bots announcement channel"""
        await interaction.response.defer(ephemeral=True)
        channel = await set_announce_channel(interaction.guild, int(channel_id))
        await interaction.followup.send(channel)   
        
    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="add_map", description="placeholder description")
    async def add_map(self, interaction: nextcord.Interaction, mapname: str) -> None:
        """creates a new map directory"""
        create_new_map_dir(interaction.guild_id, mapname)
        await interaction.send(f"New Directory created for {mapname}")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="load_traderconfig", description="placeholder description")
    async def load_traderconfig(self, interaction: nextcord.Interaction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild_id)
        if options:
            await interaction.send(view=load_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="kill", description="placeholder description")
    async def kill(self, interaction: nextcord.Interaction) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(f"Shutdown Command sent from {interaction.author}")
        await self.bot.db.close()
        await self.bot.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_key", description="placeholder description")
    async def get_key(self, interaction: nextcord.Interaction, mapname: str) -> None:
        """Looks up the given maps passkey"""
        passkey = get_map_key(interaction.guild_id, mapname)["passkey"]
        await interaction.send(embed=key_embed(mapname, passkey))

    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="remove_map", description="placeholder description")
    async def remove_map(self, interaction: nextcord.Interaction) -> None:
        """Opens the map deletion Modal"""
        await interaction.channel.send("Select a map to remove:", view=RemoveMapModal())


def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))