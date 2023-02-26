import datetime
from os import getenv
from typing import Optional

import aiohttp
from nextcord.ui import Modal, TextInput
from nextcord import Interaction
from src.discord.bot import DiscordBot


class EnterSteamID(Modal):
    """
    A modal for entering a Steam 64 ID.
    """
    def __init__(self) -> None:
        """
        Initializes the EnterSteamID modal.
        """
        super().__init__(title="Registration Form", timeout=(5 * 60))
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

        # Verify the user with the given Steam 64 ID and Discord User ID.
        new_commit = await verify_user(interaction.bot, steam_id, interaction.author.id)

        # If the verification is successful, respond with a success message.
        if new_commit == 1:
            await interaction.followup.send("Success! thank you for registering.")
        # If the verification fails, respond with a failure message.
        elif new_commit == -1:
            await interaction.followup.send(f"Fail! it looks like that account is already registered: `{steam_id}`")
        elif new_commit == -2:
            await interaction.followup.send(f"Fail! it looks like you are already registered: `{steam_id}`")
        else:
            await interaction.followup.send(f"Fail! verify you entered the Steam 64 ID correctly: `{steam_id}`")


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
    # Check if discord id is already associated with a steam id in the database
    existing_steam_id = await bot.sql_execute(
        "SELECT steam_id FROM registration WHERE discord_id=%s", (discord_id,)
    )

    # Check if steam id is already associated with a discord id in the database
    existing_discord_id = await bot.sql_execute(
        "SELECT discord_id FROM registration WHERE steam_id=%s", (steam_id,)
    )

    if existing_discord_id is not None:
        # Steam id already associated with a discord id
        return -1
    if existing_steam_id is not None:
        # Discord id already associated with a steam id
        return -2

    # Get user location information from Steam API
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={getenv("STEAM_API_KEY")}&steamids={steam_id}') as response:
            if response.status != 200:
                # Handle error response
                return -3

            data = await response.json()
            user_info = data['response']['players'][0]

            # Insert new user data into database
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await bot.sql_execute("INSERT INTO registration (discord_id, steam_id, loccountrycode, profile_url, registration_date) VALUES (%s, %s, %s, %s, %s)", discord_id, steam_id, user_info.get('loccountrycode', None), user_info.get('profileurl', None), current_time)
            return 1
