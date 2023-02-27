import json
import os
import aioftp
import aiofiles
from os import getenv
from typing import Dict

# Maps the name of a map to a port number
port_by_name: Dict[str, int] = {
    "Chernarus": 21,
    "Takistan": 22,
    "Namalsk": 23,
    "TestServer": 24
}

class FTPConnect:
    """A class to manage connections to an FTP server and perform file transfers.

    Attributes:
        host (str): The host address of the FTP server.
        port (int): The port number to connect to on the FTP server.
        user (str): The username to use when authenticating with the FTP server.
        passwd (str): The password to use when authenticating with the FTP server.
        pool (aioftp.ConnectionPool): A connection pool to manage connections to the FTP server.
    """
    def __init__(self):
        """Initializes an FTPConnect object with default values for its attributes."""
        self.ports_listing = port_by_name
        self.is_ready = False
        self.host: str = getenv("FTP_HOST")
        self.user: str = getenv("FTP_USER")
        self.passwd: str = getenv("FTP_PASSWORD")
        self.clients: dict[aioftp.Client] = {}

    async def init_ftp(self, map_name: str) -> aioftp.Client:
        """Initializes the connection pool for the FTP server.

        Args:
            map_name (str): The name of the map to connect to on the FTP server.

        Raises:
            aioftp.errors.ClientError: If the connection pool could not be created.
        """
        client: aioftp.Client = aioftp.Client()
        await client.connect(self.host, port_by_name[map_name])
        await client.login(self.user, self.passwd)
        self.clients[map_name] = client
        print(f"FTP Connection made to {self.host}:{port_by_name[map_name]} for {map_name}")




    async def get_all_player_atm(self, map_name):
        current_client: aioftp.Client = self.clients[map_name]
        print(await current_client.get_current_directory())
        await current_client.change_directory("/profiles/LBmaster/Data/LBBanking/players")
        stats = await current_client.list()
        print(stats)

        # async with current_client.download_stream("/profiles/LBmaster/Data/LBBanking/Players") as stream:
        #     async for block in stream.iter_by_block():
        #         pass

    async def get_one_player_atm(self, map_name, SK64):
        pass