from disnake.ext.commands import Bot

from src.file_manager import create_new_server_dir, initial_dir_setup


class MyClient(Bot):
    async def on_ready(self):
        initial_dir_setup()
        print("Connected to:")
        for guild in self.guilds:
            print('\t', guild.name)
            create_new_server_dir(guild.id)
        print(f'Logged on as: {self.user}')
