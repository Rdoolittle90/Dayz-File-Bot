import datetime
from os import getenv
import random
from typing import Optional
import re

import aiohttp
from discord import Embed
from nextcord.ui import Modal, TextInput
from nextcord import Interaction
from src.helpers.update_player_atm import update_money
from src.helpers.colored_printing import colorized_print
from src.discord.bot import DiscordBot


class EnterSteamID(Modal):
    """
    A modal for entering a Steam 64 ID.
    """
    map_str = {
        "0": "Chernarus",
        "1": "Takistan",
        "2": "Namalsk"
    }
    def __init__(self, bot: DiscordBot) -> None:
        """
        Initializes the EnterSteamID modal.
        """
        super().__init__(title="Registration Form", timeout=(5 * 60))
        self.bot: DiscordBot = bot

        self.steam_id = TextInput(
                label="Steam 64 ID",
                placeholder="00000000000000000",
                custom_id=f"steam_id_{random.randint(1, 99999)}",
                min_length=17,
                max_length=17,
                required=True
            )
        self.add_item(self.steam_id)

        self.map_id = TextInput(
                label="Steam 64 ID",
                placeholder="Chernarus = 0, Takistan = 1, Namalask = 3",
                custom_id=f"map_{random.randint(1, 99999)}",
                min_length=1,
                max_length=1,
                required=True
            )
        self.add_item(self.map_id)


    async def callback(self, interaction: Interaction) -> None:
        """
        Validates the Steam 64 ID entered by the user and saves it to the database.

        Args:
            interaction (ModalInteraction): The user's interaction with the modal.
        """
        await interaction.response.defer(ephemeral=True)
        steam_id = self.steam_id.value
        
        if not is_valid_steam64_id(steam_id): # 
            await interaction.followup.send(embed=embed_invalid_id(interaction.user.name, steam_id))
            return -1

        # Verify the user with the given Steam 64 ID and Discord User ID.
        new_commit = await verify_user(self.bot, steam_id, interaction.user.id)

        gift_map_name = EnterSteamID.map_str[self.map_id.value]
        print(gift_map_name)

        if new_commit == 1: # Success
            await interaction.followup.send(embed=embed_success(interaction.user.name))
            player_path = f"_files/maps/{gift_map_name}/atms/{interaction.user}.json"
            player_atm = await self.bot.ftp_connections[gift_map_name].download_one_map_file_async("atm", steam_id)
            try:
                update_money(player_atm, player_path, 50000)
                await self.bot.ftp_connections[gift_map_name].upload_file(player_path, "atm", f"{steam_id}.json")
                colorized_print("INFO", f"🟢 Registration Gift Complete ADMIN -> {interaction.user.mention}: 50000")
            except TypeError:
                colorized_print("ERROR", f"🔴 Registration Gift Failed {interaction.user.mention}")

        elif new_commit == -1: # Steam 64 ID already claimed
            await interaction.followup.send(embed=embed_already_taken(interaction.user.name))
        elif new_commit == -2: # Already registered
            await interaction.followup.send(embed=embed_already_registered(interaction.user.name))
        else: # Account not found: steam 64 was valid but not found
            await interaction.followup.send(embed=embed_invalid_id(interaction.user.name, steam_id))


async def verify_user(bot: DiscordBot, steam_id: str, discord_id: str) -> Optional[int]:
    """
    Verifies the user's Steam ID by checking if their Discord ID is already associated with a Steam ID in the database and
    saves the Steam ID and user location information to the database if verification is successful.

    Args:
        bot (DiscordBot): The bot instance.
        steam_id (str): The user's Steam 64 ID.
        discord_id (str): The user's Discord ID.

    Returns:
        1 if verification is successful,
        -1 if Steam ID is already associated with a Discord ID,
        -2 if Discord ID is already associated with a Steam ID,
        -3 if there is an error with the Steam API.
    """

    if await get_registered_steam_64(bot, discord_id) is not None:
        # Steam id already associated with a discord id
        colorized_print("WARNING", f"Discord ID {discord_id} is already associated with a Steam ID.")
        return -1
    if await get_registered_discord_id(bot, steam_id) is not None:
        # Discord id already associated with a steam id
        colorized_print("WARNING", f"Steam ID {steam_id} is already associated with a Discord ID.")
        return -2

    # Get user location information from Steam API
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={getenv("STEAM_API_KEY")}&steamids={steam_id}') as response:
                if response.status != 200:
                    # Handle error response
                    colorized_print("ERROR", f"Error getting user info from Steam API: {response.status}")
                    return -3

                data = await response.json()
                user_info = data['response']['players'][0]

                # Insert new user data into database
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                await bot.sql.sql_execute("INSERT INTO registration (discord_id, steam_id, loccountrycode, profile_url, registration_date) VALUES (%s, %s, %s, %s, %s)", discord_id, steam_id, user_info.get('loccountrycode', None), user_info.get('profileurl', None), current_time)
                colorized_print("INFO", f"User with Discord ID {discord_id} and Steam ID {steam_id} has been verified and registered.")
                return 1
    except Exception as e:
        # Handle other exceptions
        colorized_print("ERROR", f"Error verifying user with Discord ID {discord_id} and Steam ID {steam_id}: {e}")
        return -3



async def get_registered_steam_64(bot: DiscordBot, discord_id: str):
    steam_id = await bot.sql.sql_execute(
        "SELECT steam_id FROM registration WHERE discord_id=%s", (discord_id,)
    )
    if steam_id:
        return steam_id[0][0]
    else:
        return None


async def get_registered_discord_id(bot: DiscordBot, steam_id: str):
    discord_id = await bot.sql.sql_execute(
        "SELECT discord_id FROM registration WHERE steam_id=%s", (steam_id,)
    )
    if discord_id:
        return discord_id[0][0]
    else:
        return None


def is_valid_steam64_id(steam_id: str) -> bool:
    """
    Returns True if the given string matches the pattern for a valid Steam64 ID, False otherwise.
    """
    pattern = r'^\d{17}$'
    return bool(re.match(pattern, steam_id))


def embed_invalid_id(user_name, steam_id: str) -> Embed:
    colorized_print("WARNING", f"{user_name} Invalid Steam 64 ID: {steam_id}")
    embed = Embed(title="Registration Failed", color=0xff0000)
    embed.description = f"Invalid Steam 64 ID: `{steam_id}`"
    return embed


def embed_already_registered(user_name) -> Embed:
    colorized_print("WARNING", f"{user_name} is already registered")
    embed = Embed(title="Registration Failed", color=0xff0000)
    embed.description = f"You are already registered"
    return embed


def embed_already_taken(user_name) -> Embed:
    colorized_print("CRITICAL", f"{user_name} attempted to activate a Steam account that is already registered")
    embed = Embed(title="Registration Failed", color=0xff0000)
    embed.description = f"That account is already registered"
    return embed


def embed_success(user_name) -> Embed:
    colorized_print("INFO", f"{user_name} Registration Successful")
    embed = Embed(title="Registration Successful", color=0x00ff00)
    embed.description = "Thank you for registering."
    return embed

def embed_not_registered(user_name, command_name) -> Embed:
    colorized_print("INFO", f"{user_name} is Not Registered and cant use {command_name}")
    embed = Embed(title="Not Registered", color=0x00ff00)
    embed.description = "user /register to be able to use this command"
    return embed
