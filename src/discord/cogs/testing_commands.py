import asyncio
import datetime
import ftplib
import inspect

import nextcord
from nextcord import User
from nextcord.ext import commands
from src.discord.modals.registration import get_registered_steam_64

from src.discord.bot import DiscordBot
from src.helpers.colored_printing import colorized_print
from src.helpers.gen_string import generate_random_string
from src.helpers.update_player_atm import update_money


class TestingCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Testing"

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="test_trade", description="placeholder description 1")
    async def test_trade(self, interaction: nextcord.Interaction, player_1_map:str, player_2:User, player_2_map:str, trade_amount:int):
        maps = ["Chernarus", "Takistan", "Namalsk"]
        map_options = [nextcord.SelectOption(label=map_name, value=map_name) for map_name in maps]

        select = nextcord.ui.Select(
            placeholder="Select a map",
            options=map_options,
            max_values=1,
        )

        # Prompt the user for player 1's map selection
        await interaction.response.send_message("Please select the map for Player 1:", ephemeral=True, components=[select])

        try:
            player_1_map_selection = await self.bot.wait_for(
                "select_option", check=lambda i: i.component == select and i.user.id == interaction.user.id, timeout=30.0
            )
            player_1_map = player_1_map_selection.values[0]
        except asyncio.TimeoutError:
            await interaction.followup.send("You didn't select a map for Player 1 in time.", ephemeral=True)
            return

        # Prompt the user for player 2's map selection
        await interaction.response.send_message("Please select the map for Player 2:", ephemeral=True, components=[select])

        try:
            player_2_map_selection = await self.bot.wait_for(
                "select_option", check=lambda i: i.component == select and i.user.id == interaction.user.id, timeout=30.0
            )
            player_2_map = player_2_map_selection.values[0]
        except asyncio.TimeoutError:
            await interaction.followup.send("You didn't select a map for Player 2 in time.", ephemeral=True)
            return
        
        await interaction.followup.send(embed=await player_trade(self.bot, interaction.user.id, player_1_map, player_2, player_2_map, trade_amount))



async def player_trade(bot: DiscordBot, player_1:User, player_1_map:str, player_2:User, player_2_map:str, trade_amount:int):
    trade_id = generate_random_string(7)
    remote_path = '/profiles/LBmaster/Data/LBBanking/Players'
    proceed_with_trade = True

    player_1_steam_64_id = await get_registered_steam_64(bot, player_1.id)
    if player_1_steam_64_id is None:
        proceed_with_trade = False

    player_2_steam_64_id = await get_registered_steam_64(bot, player_2.id)
    if player_2_steam_64_id is None:
        proceed_with_trade = False

    if trade_amount >= 10000:
        reason = "Trade must be less than 500 rubles"
        proceed_with_trade = False
    if trade_amount <= 500:
        reason = "Trade must be greater than 500 rubles"
        proceed_with_trade = False

    player_1_success = False
    player_2_success = False
    if proceed_with_trade:
        try:
            # Player 1
            player_1_path = f"_files/maps/{player_1_map}/atms/{player_1_steam_64_id}.json"
            player_1_atm = await bot.ftp_connections[player_1_map].download_one_map_atm_file_async(player_1_steam_64_id)
            reason = update_money(player_1_atm, player_1_path, -trade_amount)
            await bot.ftp_connections[player_1_map].upload_file(player_1_path, remote_path, f"{player_1_steam_64_id}.json")
            player_1_success = True

            # Player 2
            player_2_path = f"_files/maps/{player_2_map}/atms/{player_2}.json"
            player_2_atm = await bot.ftp_connections[player_2_map].download_one_map_atm_file_async(player_2)
            update_money(player_2_atm, player_2_path, trade_amount)
            await bot.ftp_connections[player_2_map].upload_file(player_2_path, remote_path, f"{player_2_steam_64_id}.json")
            colorized_print("INFO", f"trade_id: {trade_id} 🟢 Trade Complete {player_1.mention} -> {player_2.mention}: {trade_amount}")
            player_2_success = True

        except ftplib.error_perm:
            colorized_print("ERROR", f"trade_id: {trade_id} 🔴 Trade Failed {player_1.mention} -> {player_2.mention}: {trade_amount}")
            if player_1_success == True and player_2_success == False:
                update_money(player_1_atm, player_1_path, trade_amount)
                await bot.ftp_connections[player_1_map].upload_file(player_1_path, remote_path, f"{player_1_steam_64_id}.json")
                colorized_print("DEBUG", f"trade_id: {trade_id} 🟡 Trade Value returned to sender {player_1_steam_64_id}: {trade_amount}")

    embed = nextcord.Embed(title="Trade Information")
    embed.add_field(name="Player 1", value=player_1, inline=True)
    embed.add_field(name="Player 2", value=player_2, inline=True)
    embed.set_footer(text=f"TRADE ID: {trade_id}")
    embed.add_field(name="Trade Amount", value=trade_amount)

    if player_1_success and player_2_success:
        embed.description = f"Trade Successful 🟢"
        embed.color = nextcord.Color.green()
    elif not player_1_success and not player_2_success:
        embed.description = f"Trade Cancelled 🟠 {reason}"
        embed.color = nextcord.Color.orange()
    else:
        embed.description = f"Trade Failed 🔴"
        embed.color = nextcord.Color.red()
    return embed

def setup(bot: commands.Bot):
    bot.add_cog(TestingCog(bot))
    



