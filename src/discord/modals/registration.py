import datetime
from os import getenv
from typing import Optional
import re

import aiohttp
from discord import Embed
from nextcord.ui import Modal, TextInput
from nextcord import Interaction
from src.discord.bot import DiscordBot


class EnterSteamID(Modal):
    """
    A modal for entering a Steam 64 ID.
    """
    def __init__(self, bot: DiscordBot) -> None:
        """
        Initializes the EnterSteamID modal.
        """
        super().__init__(title="Registration Form", timeout=(5 * 60))
        self.bot: DiscordBot = bot

        self.steam_id = TextInput(
                label="Steam 64 ID",
                placeholder="00000000000000000",
                custom_id="map",
                min_length=17,
                max_length=17,
                required=True
            )
        self.add_item(self.steam_id)


    async def callback(self, interaction: Interaction) -> None:
        """
        Validates the Steam 64 ID entered by the user and saves it to the database.

        Args:
            interaction (ModalInteraction): The user's interaction with the modal.
        """
        await interaction.response.defer(ephemeral=False)
        steam_id = self.steam_id.value
        
        if not is_valid_steam64_id(steam_id): # 
            await interaction.followup.send(embed=embed_invalid_id(steam_id))
            return -1

        # Verify the user with the given Steam 64 ID and Discord User ID.
        new_commit = await verify_user(self.bot, steam_id, interaction.user.id)

        if new_commit == 1: # Success
            await interaction.followup.send(embed=embed_success())
        elif new_commit == -1: # Steam 64 ID already claimed
            await interaction.followup.send(embed=embed_already_taken())
        elif new_commit == -2: # Already registered
            await interaction.followup.send(embed=embed_already_registered())
        else: # Account not found: steam 64 was valid but not found
            await interaction.followup.send(embed=embed_invalid_id(steam_id))


async def verify_user(bot: DiscordBot, steam_id: str, discord_id: str) -> Optional[int]:
    """
    Verifies the user's Steam ID by checking if their Discord ID is already associated with a Steam ID in the database and
    saves the Steam ID and user location information to the database if verification is successful.

    Args:
        bot (DiscordBot): The bot instance.
        steam_id (str): The user's Steam 64 ID.
        discord_id (str): The user's Discord ID.

    Returns:
        1 if verification is successful,\n
        -1 if Steam ID is already associated with a Discord ID,\n
        -2 if Discord ID is already associated with a Steam ID,\n
        -3 if there is an error with the Steam API.
    """

    if await get_registered_steam_64(bot, discord_id) is None:
        # Steam id already associated with a discord id
        return -1
    if await get_registered_discord_id(bot, steam_id) is None:
        # Discord id already associated with a steam id
        return -2

    # Get user location information from Steam API
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={getenv("STEAM_API_KEY")}&steamids={steam_id}') as response:
                if response.status != 200:
                    # Handle error response
                    return -3

                data = await response.json()
                user_info = data['response']['players'][0]

                # Insert new user data into database
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                await bot.sql_execute("INSERT INTO registration (discord_id, steam_id, loccountrycode, profile_url, registration_date) VALUES (%s, %s, %s, %s, %s)", discord_id, steam_id, user_info.get('loccountrycode', None), user_info.get('profileurl', None), current_time)
                return 1
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return -3



async def get_registered_steam_64(bot, discord_id):
    steam_id = await bot.sql_execute(
        "SELECT steam_id FROM registration WHERE discord_id=%s", (discord_id,)
    )
    return steam_id


async def get_registered_discord_id(bot, steam_id):
    discord_id = await bot.sql_execute(
        "SELECT discord_id FROM registration WHERE steam_id=%s", (steam_id,)
    )
    return discord_id


def is_valid_steam64_id(steam_id: str) -> bool:
    """
    Returns True if the given string matches the pattern for a valid Steam64 ID, False otherwise.
    """
    pattern = r'^\d{17}$'
    return bool(re.match(pattern, steam_id))


def embed_invalid_id(steam_id) -> Embed:
    embed = Embed(title="Registration Failed", color=0xff0000)
    embed.description = f"Invalid Steam 64 ID: `{steam_id}`"
    return embed


def embed_already_registered() -> Embed:
    embed = Embed(title="Registration Failed", color=0xff0000)
    embed.description = f"You are already registered"
    return embed


def embed_already_taken() -> Embed:
    embed = Embed(title="Registration Failed", color=0xff0000)
    embed.description = f"That account is already registered"
    return embed

def embed_success() -> Embed:
    embed = Embed(title="Registration Successful", color=0x00ff00)
    embed.description = "Thank you for registering."
    return embed