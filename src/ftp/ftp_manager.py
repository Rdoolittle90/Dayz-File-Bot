import datetime
import logging
import os
import random
import aioftp
from typing import Dict

from src.helpers.colored_logging import colorize_log

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
        user (str): The username to use when authenticating with the FTP server.
        passwd (str): The password to use when authenticating with the FTP server.
    """

    def __init__(self):
        """Initializes an FTPConnect object with default values for its attributes."""
        self.host: str = os.getenv("FTP_HOST")
        self.user: str = os.getenv("FTP_USER")
        self.passwd: str = os.getenv("FTP_PASSWORD")

    def my_parser(filename):
        dt_str = filename.split("_")[1]
        dt = datetime.datetime.strptime(dt_str, "%Y%m%d_%H%M%S")
        return dt
    
    async def get_all_player_atm(self, map_name):
        """
        Connects to an FTP server and downloads all JSON files in the /profiles/LBmaster/Data/LBBanking/Players directory.

        Args:
            map_name (str): The name of the map to download the JSON files for.

        Raises:
            aioftp.StatusCodeError: If the FTP server returns an error status code.

        Returns:
            None
        """
        async with aioftp.Client.context(self.host, port_by_name[map_name], self.user, self.passwd) as client:
            client.parser = self.my_parser
            colorize_log("INFO", f"Connecting to {self.host}:{port_by_name[map_name]} {map_name}  {random.randint(0, 99999)}")
            try:
                for path, info in await client.list():
                    if info["type"] == "file" and path.suffix == ".json":
                        colorize_log("INFO", f"Downloading file {path.name}")
            except ValueError as err:
                colorize_log("ERROR", f"Error: {err.message}")


    async def get_one_player_atm(self, map_name, SK64):
        pass