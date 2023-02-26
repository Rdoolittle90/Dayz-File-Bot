from nextcord import SlashCommand, SlashContext, MemberPermissions, PermissionOverwrite
from nextcord.ext.commands import Cog
from nextcord import Bot

from src.discord.announcements import announce_status
from src.discord.guild_manager import get_map_selections
from src.discord.load_traderconfig import load_traderconfig_view
from src.discord.modals.remove_map_modal import RemoveMapModal
from src.file_manager import create_new_map_dir, get_map_key, key_embed


class AdminCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin Cog Connected")

    # =====================================================================================================
    @SlashCommand(name="set_status", description="", default_permission=False)
    async def set_status(self, ctx: SlashContext, status_code: int, map_name: str = "ALL", message: str = None):
        """status_codes: 0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
        await announce_status(ctx, status_code, map_name, message)

    # =====================================================================================================
    @SlashCommand(name="add_map", description="")
    async def add_map(self, ctx: SlashContext, mapname: str) -> None:
        """creates a new map directory"""
        create_new_map_dir(ctx.guild_id, mapname)
        await ctx.send(f"New Directory created for {mapname}")

    # =====================================================================================================
    @SlashCommand(name="load_traderconfig", description="", default_permission=False)
    async def load_traderconfig(self, ctx: SlashContext) -> None:
        """Render the TraderConfig.txt for the selected map"""
        options = get_map_selections(ctx.guild_id)
        if options:
            await ctx.send(view=load_traderconfig_view(options=options), ephemeral=True)
        else:
            await ctx.send("Server has no registered maps", ephemeral=True)

    # =====================================================================================================
    @SlashCommand(name="kill", description="", default_permission=False)
    async def kill(self, ctx: SlashContext) -> None:
        """Kill the bot 🗡️🤖 requires manual reboot"""
        await ctx.send(f"Shutdown Command sent from {ctx.author}")
        await self.bot.db.close()
        await self.bot.close()  # Throws a RuntimeError noisey but seems to have no ill effect   #FIXME

    # =====================================================================================================
    @SlashCommand(name="get_key", description="", default_permission=False)
    async def get_key(self, ctx: SlashContext, mapname: str) -> None:
        """Looks up the given maps passkey"""
        passkey = get_map_key(ctx.guild_id, mapname)["passkey"]
        await ctx.send(embed=key_embed(mapname, passkey))

    # =====================================================================================================
    @SlashCommand(name="remove_map", description="", default_permission=False)
    async def remove_map(self, ctx: SlashContext) -> None:
        """Opens the map deletion Modal"""
        await ctx.channel.send("Select a map to remove:", view=RemoveMapModal())


def setup(bot: Bot):
    bot.add_cog(AdminCog(bot))