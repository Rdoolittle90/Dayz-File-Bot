import random
import nextcord
from nextcord.ext import commands

class MiniGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.symbols = {
            "Cherry": {"weight": 3, "payout": 3},
            "Orange": {"weight": 3, "payout": 3},
            "Lemon": {"weight": 3, "payout": 3},
            "Bar": {"weight": 2, "payout": 5},
            "7": {"weight": 1, "payout": 10}
        }
    
    @nextcord.slash_command(dm_permission=False, name="slots", description="Slots test")
    async def slots(self, ctx, bet: int):
        if bet <= 0:
            await ctx.send("Please enter a valid bet amount.")
            return
        
        user = ctx.author
        user_balance = 500 # replace with actual user balance
        
        if bet > user_balance:
            await ctx.send(f"You do not have enough currency to place this bet. Your current balance is {user_balance}.")
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
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="Reels", value=f"{reels[0]} | {reels[1]} | {reels[2]}", inline=False)
        embed.add_field(name="Payout", value=f"{bet * payout} currency")
        embed.add_field(name="Balance", value=f"{user_balance} currency", inline=False)
        
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(MiniGames(bot))