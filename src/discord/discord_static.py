from disnake.ext.commands import Bot
from disnake.message import Message

from src.discord.guild_manager import (check_for_files, initial_cha_setup,
                                       initial_server_setup)
from src.file_manager import create_new_server_dir, initial_dir_setup


class MyClient(Bot):
    async def on_ready(self):
        initial_dir_setup()
        print("Connected to:")
        for guild in self.guilds:
            print('\t', guild.name)
            await initial_cha_setup(guild)
            await initial_server_setup(guild)
            create_new_server_dir(guild.id)
        print(f'Logged on as: {self.user}')


    async def on_message(self, message: Message):
        if message.author != self.user:
            await check_for_files(message)