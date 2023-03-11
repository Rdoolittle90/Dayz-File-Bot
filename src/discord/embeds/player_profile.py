from os import getenv
import nextcord
import requests
from src.discord.bot import DiscordBot
from src.discord.modals.registration import get_registered_steam_64


async def create_profile_card_embed(bot: DiscordBot, discord_id) -> nextcord.Embed:
    steam_id = await get_registered_steam_64(bot, discord_id)
    print(steam_id)


    if await get_registered_steam_64(bot, discord_id) is None:
        embed = nextcord.Embed(
            title="Not registered",
            description=f"You must use /register be you are able to use this command",
            color=nextcord.Color.red()
        )
        return embed

    # Get Steam API data
    steam_api_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={getenv('STEAM_API_KEY')}&steamids={steam_id}"
    response = requests.get(steam_api_url)
    data = response.json()["response"]["players"][0]

    # Create embed
    embed = nextcord.Embed(
        title=data["personaname"],
        description=f"**Profile:** [Link]({data['profileurl']})\n",
        color=nextcord.Color.blue()
    )

    # Add thumbnail and image
    if "avatarfull" in data:
        embed.set_thumbnail(url=data["avatarfull"])
    if "gameextrainfo" in data:
        embed.set_image(url=f"https://steamcdn-a.akamaihd.net/steam/apps/{data['gameid']}/header.jpg")

    return embed