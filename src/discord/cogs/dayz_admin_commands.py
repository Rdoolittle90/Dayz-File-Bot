import datetime
from nextcord.ext import commands
import nextcord
from src.helpers.colored_printing import colorized_print
from src.discord.announcements import announce_status
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.file_manager import create_new_map_dir, get_map_key, key_embed
from src.dayz.load_traderconfig import load_traderconfig_view
from src.discord.guild_manager import get_map_selections
from src.discord.bot import DiscordBot



class DayzAdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "DayZ Admin"


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="set_status", description='"0:"OFFLINE", 1:"ONLINE", 2:"RESTARTING"')
    async def set_status(self, interaction: nextcord.Interaction, status_code: int, map_name: str = "ALL", message: str = None):
        colorized_print("INFO", f"{interaction.user.name} used DayzAdminCog.set_status at {datetime.datetime.now()}")
        """Set the status of the server to either offline, online, or restarting."""
        await announce_status(interaction, status_code, map_name, message)


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="load_traderconfig", description="Render the TraderConfig.txt for the selected map")
    async def load_traderconfig(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzAdminCog.load_traderconfig at {datetime.datetime.now()}")
        """Render the TraderConfig.txt file for the selected map."""
        options = get_map_selections()
        if options:
            await interaction.send(view=load_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="add_map", description="Create a new map directory")
    async def add_map(self, interaction: nextcord.Interaction, mapname: str) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzAdminCog.load_traderconfig at {datetime.datetime.now()}")
        """Create a new directory for the given map name."""
        create_new_map_dir(mapname)
        await interaction.send(f"New directory created for {mapname}")


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="remove_map", description="Open the map deletion modal")
    async def remove_map(self, interaction: nextcord.Interaction) -> None:
        colorized_print("WARNING", f"{interaction.user.name} used DayzAdminCog.remove_map at {datetime.datetime.now()}")
        """Open the map deletion modal."""
        await interaction.response.send_modal(modal=RemoveMapModal())


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="get_key", description="Look up the given map's passkey")
    async def get_key(self, interaction: nextcord.Interaction, mapname: str) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzAdminCog.get_key at {datetime.datetime.now()}")
        """Look up the passkey for the given map name."""
        passkey = get_map_key(mapname)["passkey"]
        await interaction.send(embed=key_embed(mapname, passkey))


def setup(bot: commands.Bot):
    bot.add_cog(DayzAdminCog(bot))
