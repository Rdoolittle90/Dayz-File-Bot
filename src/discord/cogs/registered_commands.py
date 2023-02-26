from nextcord.ext import commands
import nextcord
from src.discord.registration import EnterSteamID


class RegisteredCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin Cog Connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="placeholder description 1")
    async def register(ctx) -> None:
        """placeholder"""
        await ctx.response.send_modal(modal=EnterSteamID())


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="atm", description="placeholder description 1")
    async def atm(ctx) -> None:
        """placeholder"""
        pass


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="inventory", description="placeholder description 1")
    async def inventory(ctx) -> None:
        print(type(ctx))
        """placeholder"""
        pass


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="trade", description="placeholder description 1")
    async def trade(ctx) -> None:
        """placeholder"""
        pass


def setup(bot: commands.Bot):
    bot.add_cog(RegisteredCog(bot))