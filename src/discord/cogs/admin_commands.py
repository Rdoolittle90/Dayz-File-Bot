from disnake import ApplicationCommandInteraction, SlashCommand
from disnake.ext.commands import Cog, command
from discord.bot import DiscordBot

from src.discord.announcements import announce_status
from src.discord.guild_manager import get_map_selections
from src.discord.load_traderconfig import load_traderconfig_view
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.file_manager import create_new_map_dir, get_map_key, key_embed


class AdminCog(DiscordBot, Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin Cog Connected")

    @DiscordBot.slash_command(name="set_status", description="", default_member_permissions=8, dm_permission=False)
    async def set_status(self, ctx, status_code:int, map_name="ALL", message=None):
        """status_codes: 0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
        await announce_status(ctx, status_code, map_name, message)

    @DiscordBot.slash_command(name="add_map", description="", dm_permission=False)
    async def add_map(self, interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """creates a new map directory"""
        create_new_map_dir(interaction.guild.id, mapname)
        await interaction.send(f"New Directory created for {mapname}")

    # =====================================================================================================
    @DiscordBot.slash_command(name="load_traderconfig", description="", default_member_permissions=8, dm_permission=False)
    async def load_traderconfig(self, interaction: ApplicationCommandInteraction) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(interaction.guild.id)
        if options:
            await interaction.send(view=load_traderconfig_view(options=options), ephemeral=True)
        else:
            await interaction.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @DiscordBot.slash_command(name="kill", description="", default_member_permissions=8, dm_permission=False)
    async def kill(self, interaction:ApplicationCommandInteraction) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await interaction.send(f"Shutdown Command sent from {interaction.author}")
        await self.bot.pool.close()
        await interaction.client.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME


    # =====================================================================================================
    @DiscordBot.slash_command(name="get_key", description="", default_member_permissions=8, dm_permission=False)
    async def get_key(self, interaction:ApplicationCommandInteraction, mapname: str) -> None:
        """Looks up the given maps passkey"""
        passkey = get_map_key(interaction.guild.id, mapname)["passkey"]
        await interaction.send(embed=key_embed(mapname, passkey))
        
    # =====================================================================================================
    @DiscordBot.slash_command(name="remove_map", description="", default_member_permissions=8, dm_permission=False)
    async def remove_map(interaction:ApplicationCommandInteraction) -> None:
        """Opens the map deletion Modal"""
        await interaction.response.send_modal(modal=RemoveMapModal())



def setup(bot):
    bot.add_cog(AdminCog(bot))