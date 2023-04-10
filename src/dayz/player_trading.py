import ftplib
from nextcord import Color

import nextcord
from nextcord import User

from src.discord.bot import DiscordBot
from src.discord.modals.registration import get_registered_steam_64
from src.helpers.colored_printing import colorized_print
from src.helpers.gen_string import generate_random_string
from src.helpers.update_player_atm import update_money


async def player_trade(bot: DiscordBot, player_1:User, player_1_map:str, player_2:User, player_2_map:str, trade_amount:int):
    trade_id = generate_random_string(7)
    proceed_with_trade = True
    valid_maps = ["Chernarus", "Takistan", "Namalsk"]
    if player_1_map not in valid_maps:
        reason = f"Map Not Found: {player_1_map}\n options: {', '.join(valid_maps)}"
        proceed_with_trade = False
    if player_2_map not in valid_maps:
        reason = f"Map Not Found: {player_2_map}\n options: {', '.join(valid_maps)}"
        proceed_with_trade = False


    player_1_steam_64_id = await get_registered_steam_64(bot, player_1.id)
    if player_1_steam_64_id is None:
        reason = "You are not registered!"
        proceed_with_trade = False

    player_2_steam_64_id = await get_registered_steam_64(bot, player_2.id)
    if player_2_steam_64_id is None:
        reason = "The person you are attempting to send rubles to is not registered"
        proceed_with_trade = False

    if trade_amount >= 10000:
        reason = "Trade must be less than 10000 rubles"
        proceed_with_trade = False
    if trade_amount <= 1:
        reason = "Trade must be greater than 500 rubles"
        proceed_with_trade = False

    player_1_success = False
    player_2_success = False
    if proceed_with_trade:
        try:
            # Player 1
            player_1_path = f"_files/maps/{player_1_map}/atms/{player_1_steam_64_id}.json"
            player_1_atm = await bot.ftp_connections[player_1_map].download_one_map_file_async("atm", player_1_steam_64_id)
            reason = update_money(player_1_atm, player_1_path, -trade_amount)
            await bot.ftp_connections[player_1_map].upload_file(player_1_path, "atm", f"{player_1_steam_64_id}.json")
            player_1_success = True

            # Player 2
            player_2_path = f"_files/maps/{player_2_map}/atms/{player_2}.json"
            player_2_atm = await bot.ftp_connections[player_2_map].download_one_map_file_async("atm", player_2_steam_64_id)
            update_money(player_2_atm, player_2_path, trade_amount)
            await bot.ftp_connections[player_2_map].upload_file(player_2_path, "atm", f"{player_2_steam_64_id}.json")
            colorized_print("INFO", f"trade_id: {trade_id} 🟢 Trade Complete {player_1.mention} -> {player_2.mention}: {trade_amount}")
            player_2_success = True

        except ftplib.error_perm:
            colorized_print("ERROR", f"trade_id: {trade_id} 🔴 Trade Failed {player_1.mention} -> {player_2.mention}: {trade_amount}")
            if player_1_success == True and player_2_success == False:
                update_money(player_1_atm, player_1_path, trade_amount)
                await bot.ftp_connections[player_1_map].upload_file(player_1_path, "atm", f"{player_1_steam_64_id}.json")
                colorized_print("INFO", f"trade_id: {trade_id} 🟡 Trade Value returned to sender {player_1_steam_64_id}: {trade_amount}")

    embed = nextcord.Embed(title="Trade Information")
    embed.add_field(name=f"{player_1}  ➡️", value=player_1_map, inline=True)
    embed.add_field(name=f"{player_2}", value=player_2_map, inline=True)
    embed.add_field(name="Amount:", value=f"{trade_amount}₽")
    embed.set_footer(text=f"TRADE ID: {trade_id}")

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


async def player_give(bot: DiscordBot, player_2:User, player_2_map:str, trade_amount:int):
    trade_id = generate_random_string(7)
    proceed_with_trade = True
    valid_maps = ["Chernarus", "Takistan", "Namalsk"]
    if player_2_map not in valid_maps:
        reason = f"Map Not Found: {player_2_map}\n options: {', '.join(valid_maps)}"
        proceed_with_trade = False

    player_2_steam_64_id = await get_registered_steam_64(bot, player_2.id)
    if player_2_steam_64_id is None:
        reason = "The person you are attempting to send rubles to is not registered"
        proceed_with_trade = False
        embed = nextcord.Embed(title=reason, color=Color.red())
        return embed



    if proceed_with_trade:
        player_2_path = f"_files/maps/{player_2_map}/atms/{player_2}.json"
        player_2_atm = await bot.ftp_connections[player_2_map].download_one_map_file_async("atm", player_2_steam_64_id)
        update_money(player_2_atm, player_2_path, trade_amount)
        await bot.ftp_connections[player_2_map].upload_file(player_2_path, "atm", f"{player_2_steam_64_id}.json")
        colorized_print("INFO", f"trade_id: {trade_id} 🟢 Trade Complete ADMIN -> {player_2.mention}: {trade_amount}")
        player_2_success = True

    embed = nextcord.Embed(title="Trade Information")
    embed.add_field(name=f"{player_2}", value=player_2_map, inline=True)
    embed.add_field(name="Amount:", value=f"{trade_amount}₽")
    embed.set_footer(text=f"TRADE ID: {trade_id}")

    if player_2_success:
        embed.description = f"Trade Successful 🟢"
        embed.color = nextcord.Color.green()
    else:
        embed.description = f"Trade Failed 🔴"
        embed.color = nextcord.Color.red()
    return embed