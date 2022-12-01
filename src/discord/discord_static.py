from os import getenv
import disnake
from disnake.ext.commands import Bot


class MyClient(Bot):


    async def on_ready(self):
        print("Connected to:")
        for guild in self.guilds:
            print('\t', guild.name)
        print(f'Logged on as: {self.user}')


async def get_guild_emojis(client: MyClient):
    guild: disnake.Guild = await client.fetch_guild(getenv("DISCORD_GUILD"))
    emoji_list = {}
    for emoji in guild.emojis:
        emoji_list[emoji.name] = emoji
    return emoji_list