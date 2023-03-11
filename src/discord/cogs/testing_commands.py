import datetime
import inspect

from nextcord import Interaction, User, slash_command
import nextcord
from nextcord.ext import commands
from src.discord.modals.registration import get_registered_steam_64

from src.dayz.player_trading import player_trade
from src.discord.bot import DiscordBot
from src.helpers.colored_printing import colorized_print


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Testing"

    # =====================================================================================================
    @slash_command(dm_permission=False, name="test_trade", description="placeholder description 1")
    async def test_trade(self, interaction: Interaction, player_1_map:str, player_2:User, player_2_map:str, trade_amount:int):
        colorized_print("WARNING", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(embed=await player_trade(self.bot, interaction.user, player_1_map.title(), player_2, player_2_map.title(), trade_amount))


   # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_killboard", description="placeholder description 1")
    async def get_killboard(self, interaction: nextcord.Interaction, map_name:str=None):
        colorized_print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer(ephemeral=False)
        self.bot.ftp_connections[map_name].download_one_map_killboard_file_async(await get_registered_steam_64(self.bot, interaction.user))





def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))
    



