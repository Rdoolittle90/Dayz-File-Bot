from nextcord.ext import commands
import nextcord
from src.discord.modals.registration import EnterSteamID
from src.discord.bot import DiscordBot



class DayzUserCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Dayz User Cog Connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="register your steam 64 ID")
    async def register(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="atm", description="View your ATMs")
    async def atm(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="inventory", description="View your discord item inventory")
    async def inventory(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="trade", description="Trade Discord Stashed items")
    async def trade(self, interaction: nextcord.Interaction) -> None:
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DayzUserCog(bot))