import random
import nextcord
from nextcord.ext import commands

class MiniGames(commands.Cog):
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
        print("Minigame Cog Connected")
    
    @nextcord.slash_command(dm_permission=False, name="slots", description="Slots test")
    async def slots(self, interaction, bet: int):
        if bet <= 0:
            await interaction.channel.send("Please enter a valid bet amount.")
            return
        
        user_balance = 500 # replace with actual user balance
        
        if bet > user_balance:
            await interaction.channel.send(f"You do not have enough currency to place this bet. Your current balance is {user_balance}.")
            return
        
        user_balance -= bet
        
        reels = []
        for _ in range(3):
            reels.append(random.choices(list(self.symbols.keys()), weights=list(x["weight"] for x in self.symbols.values()), k=1)[0])
        
        payout_multiplier = 1
        if reels[0] == reels[1] == reels[2]:
            payout_multiplier = 3
        
        elif reels[0] == reels[1] or reels[1] == reels[2]:
            payout_multiplier = 2
        
        payout = sum(self.symbols[symbol]["payout"] * payout_multiplier for symbol in reels)
        user_balance += bet * payout
        
        embed = nextcord.Embed(title="DayZ Slot Machine", color=0xff0000)
        embed.add_field(name="Reels", value=f"{reels[0]} | {reels[1]} | {reels[2]}", inline=False)
        embed.add_field(name="Payout", value=f"{bet * payout} currency")
        embed.add_field(name="Balance", value=f"{user_balance} currency", inline=False)
        
        await interaction.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(MiniGames(bot))