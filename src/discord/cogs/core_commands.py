from nextcord.ext import commands
import nextcord
from discord.bot import DiscordBot

from src.discord.modals.registration import EnterSteamID



class EveryoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        print("Everyone Cog Connected")


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def kill(self, interaction: nextcord.Interaction) -> None:
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()


def setup(bot: commands.Bot):
    bot.add_cog(EveryoneCog(bot))