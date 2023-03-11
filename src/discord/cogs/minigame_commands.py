import datetime
import inspect
import random
from typing import List
import discord
from nextcord.ext import commands
import nextcord
from src.discord.bot import DiscordBot
from src.discord.modals.registration import embed_not_registered, get_registered_steam_64
from src.helpers.update_player_atm import update_money

from src.helpers.colored_printing import colorized_print


class Minigames(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.symbols = {
            "🩹": {"weight": 10, "payout": 0.0},  # Bandage 0
            "💉": {"weight": 10, "payout": 0.3},  # Morphine 0.3
            "🍔": {"weight": 10, "payout": 0.5},  # Food 0.5
            "🔪": {"weight": 8, "payout": 0.7},   # Knife 0.7
            "🎒": {"weight": 5, "payout": 1.0},  # Backpack 1.0
            "🔫": {"weight": 3, "payout": 1.5},  # Gun 1.5
            "🚗": {"weight": 2, "payout": 2.5},  # Vehicle 2.5
            "🚁": {"weight": 1, "payout": 5.0},  # Helicopter 5.0
        }
        self.name = "Minigames"


    @nextcord.slash_command(dm_permission=False, name="slot", description="WIP")
    async def slot(self, interaction: nextcord.Interaction, map_name:str, bet:int):
        colorized_print("INFO", f"{interaction.user.name} used {self.__cog_name__}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Play the slot machine!"""
        await interaction.response.defer(ephemeral=False)
        player_steam_64_id = await get_registered_steam_64(self.bot, interaction.user.id)
        if player_steam_64_id is None:
            reason = "You are not registered!"
            balance:int = 0
            await interaction.followup.send(embed=embed_not_registered(interaction.user.name, self.__cog_name__))
        else:
            player_path = f"_files/maps/{map_name}/atms/{player_steam_64_id}.json"
            player_atm = await self.bot.ftp_connections[map_name].download_one_map_file_async("atm", player_steam_64_id)
            balance = update_money(player_atm, player_path, 0)


        if balance < bet:
            await interaction.followup.send("You don't have enough money to place that bet!")
            return

        spin_result = self._get_spin_result()
        colorized_print("DEBUG", f"{interaction.user.name} spin result {spin_result}")
        payout = self._calculate_payout(bet, spin_result)
        colorized_print("DEBUG", f"{interaction.user.name} received {payout}")

        update_money(player_atm, player_path, payout - bet)
        await self.bot.ftp_connections[map_name].upload_file(player_path, "atm", f"{player_steam_64_id}.json")

        embed = discord.Embed(title="Slot Machine", description=f"{' '.join(spin_result)}", color=discord.Color.blue())
        embed.add_field(name="Payout", value=f"{payout} credits")
        embed.add_field(name="Balance", value=f"{balance} credits")

        await interaction.followup.send(embed=embed)


    def _get_spin_result(self) -> List[str]:
        spin_result = []
        for i in range(3):
            symbol = random.choices(
                list(self.symbols.keys()),
                weights=[symbol["weight"] for symbol in self.symbols.values()],
                k=1
            )[0]
            spin_result.append(symbol)
        return spin_result

    def _calculate_payout(self, bet, spin_result: List[str]) -> int:
        payout = 0
        for symbol in spin_result:
            payout += bet * self.symbols[symbol]["payout"]
        return payout


def setup(bot: commands.Bot):
    bot.add_cog(Minigames(bot))