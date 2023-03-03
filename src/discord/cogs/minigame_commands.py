import random
from typing import List
import discord
from nextcord.ext import commands
import nextcord

class Minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.symbols = {
            "🩹": {"weight": 10, "payout": 2},  # Bandage
            "💉": {"weight": 10, "payout": 3},  # Morphine
            "🍔": {"weight": 10, "payout": 5},  # Food
            "🔪": {"weight": 8, "payout": 7},   # Knife
            "🎒": {"weight": 5, "payout": 10},  # Backpack
            "🔫": {"weight": 3, "payout": 15},  # Gun
            "🚗": {"weight": 2, "payout": 25},  # Vehicle
            "🚁": {"weight": 1, "payout": 50},  # Helicopter
        }

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

    def _calculate_payout(self, spin_result: List[str]) -> int:
        payout = 0
        for symbol in spin_result:
            payout += self.symbols[symbol]["payout"]
        return payout

    @nextcord.slash_command(dm_permission=False, name="slot", description="WIP")
    async def slot(self, ctx, bet):
        """Play the slot machine!"""
        balance = 500
        if balance < bet:
            await ctx.channel.send("You don't have enough money to place that bet!")
            return

        spin_result = self._get_spin_result()
        payout = self._calculate_payout(spin_result)

        balance += payout - bet

        embed = discord.Embed(title="Slot Machine", description=f"{' '.join(spin_result)}", color=discord.Color.blue())
        embed.add_field(name="Payout", value=f"{payout} credits")
        embed.add_field(name="Balance", value=f"{balance} credits")

        await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Minigames(bot))