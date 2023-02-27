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
        self.host: str = getenv("FTP_HOST")
        self.user: str = getenv("FTP_USER")
        self.passwd: str = getenv("FTP_PASSWORD")
        

    async def get_all_player_atm(self, map_name):
        async with aioftp.Client.context(self.host, port_by_name[map_name], self.user, self.passwd) as client:
            print(f"Connecting to {self.host}:{port_by_name[map_name]} {map_name}")
            async with aioftp.setlocale("C"):
                try:
                    async for path, info in client.list("profiles/LBmaster/Data/LBBanking/players/"):
                        if info["type"] == "file" and path.suffix == ".json":
                            print(path)
                except aioftp.StatusCodeError as e:
                    print(f"Error: {e.message}")

    async def get_one_player_atm(self, map_name, SK64):
        pass