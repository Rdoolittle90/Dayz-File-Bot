import datetime
import inspect
import json

import nextcord
from nextcord import (Button, ButtonStyle, Embed, Interaction, User,
                      slash_command)
from nextcord.ext import commands

from src.dayz.player_trading import player_give, player_trade
from src.discord.bot import DiscordBot
from src.helpers.colored_printing import colorized_print


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Testing"

    # =====================================================================================================
    @slash_command(dm_permission=False, name="trade", description="placeholder description 1")
    async def trade(self, interaction: Interaction, player_1_map:str, player_2:User, player_2_map:str, trade_amount:int):
        colorized_print("WARNING", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer(ephemeral=False)
        try:
            embed = await player_trade(self.bot, interaction.user, player_1_map.title(), player_2, player_2_map.title(), trade_amount)
        except:
            raise commands.CommandError('Something went wrong.')
        await interaction.followup.send(embed=embed)

    # =====================================================================================================
    @slash_command(dm_permission=False, name="trade", description="placeholder description 1")
    async def give(self, interaction: Interaction, player_2:User, player_2_map:str, trade_amount:int):
        colorized_print("WARNING", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer(ephemeral=False)
        try:
            embed = await player_give(self.bot, player_2, player_2_map.title(), trade_amount)
        except:
            raise commands.CommandError('Something went wrong.')
        await interaction.followup.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))
