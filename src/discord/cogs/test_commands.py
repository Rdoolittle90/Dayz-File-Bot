import asyncio
from nextcord.ext import commands
import nextcord



class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("!!! Testing Cog Connected !!!")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="debug_atm_get_all", description="placeholder description 1")
    async def debug_atm_get_all(self, interaction: nextcord.Interaction):
        """placeholder method"""
        tasks = [
            asyncio.create_task(self.bot.ftp.get_all_player_atm("Chernarus")),
            asyncio.create_task(self.bot.ftp.get_all_player_atm("Takistan")),
            asyncio.create_task(self.bot.ftp.get_all_player_atm("Namalsk")),
            asyncio.create_task(self.bot.ftp.get_all_player_atm("TestServer"))
        ]
        await asyncio.wait(tasks)


def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))