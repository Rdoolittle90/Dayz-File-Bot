import datetime
from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import BucketType
from src.helpers.colored_printing import colorized_print
from src.discord.embeds.player_profile import create_profile_card_embed
from src.discord.modals.registration import EnterSteamID
from src.discord.bot import DiscordBot



class DayzUserCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "DayZ User"

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="register your steam 64 ID")
    async def register(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzUserCog.register at {datetime.datetime.now()}")
        """placeholder"""
        await interaction.response.send_modal(modal=EnterSteamID(self.bot))


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="profile", description="View your player card")
    async def profile(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzUserCog.profile at {datetime.datetime.now()}")
        """placeholder"""
        await interaction.channel.send(embed=await create_profile_card_embed(self.bot, interaction.user.id))


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="atm", description="View your ATMs")
    async def atm(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzUserCog.atm at {datetime.datetime.now()}")
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="inventory", description="View your discord item inventory")
    async def inventory(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzUserCog.inventory at {datetime.datetime.now()}")
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


    # =====================================================================================================
    @commands.has_role("Steam Linked")
    @nextcord.slash_command(dm_permission=False, name="trade", description="Trade Discord Stashed items")
    async def trade(self, interaction: nextcord.Interaction) -> None:
        colorized_print("INFO", f"{interaction.user.name} used DayzUserCog.trade at {datetime.datetime.now()}")
        """placeholder"""
        embed = nextcord.Embed(title="Unavailable", color=0xff0000)
        embed.description = f"Command Coming Soon"
        await interaction.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DayzUserCog(bot))