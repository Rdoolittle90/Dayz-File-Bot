from disnake import ApplicationCommandInteraction, Color, Embed
import datetime

from src.discord.guild_manager import get_server_settings


async def announce_status(interaction:ApplicationCommandInteraction, status_code:int, map:str ="ALL", message:str=None) -> Embed:
    """status_codes: 
    0: "OFFLINE", 1: "ONLINE", 2: "RESTARTING" """
    
    if map == "ALL":
        server_str_format = "**SERVERS** are"
    else:
        server_str_format = "**SERVER** is"

    if status_code == 0:
        embed = Embed(title=f"**{map} {server_str_format} **DOWN", description=message, timestamp=datetime.datetime.now(), color=Color.red())
        embed.set_author(name=interaction.author, icon_url=interaction.author.avatar.url)
    elif status_code == 1:
        embed = Embed(title=f"**{map}** {server_str_format} now **ONLINE**", description=message, timestamp=datetime.datetime.now(), color=Color.green())
        embed.set_author(name=interaction.author, icon_url=interaction.author.avatar.url)
    else:
        embed = Embed(title=f"**{map}** {server_str_format} now **RESTARTING**", description=message, timestamp=datetime.datetime.now(), color=Color.yellow())
        embed.set_author(name=interaction.author, icon_url=interaction.author.avatar.url)

    settings = get_server_settings(interaction.guild.id)
    if settings["announcement_channel"] != None:
        channel = await interaction.guild.fetch_channel()
        channel.send(embed=embed)
        await interaction.send("Complete.", ephemeral=True)
    else:
        await interaction.send("No announcement channel set use /set_announcement_channel `channel ID`", ephemeral=True)