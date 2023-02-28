import datetime
import json
import os
import random
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
        
    def my_parse_list_line(line):
        """
        A custom parsing function to handle the server response when the MLSD/MLST commands are not supported.

        This function is intended to parse the server response of a 'LIST' command.
        """

        # Replace the month abbreviation with its number
        months = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }
        line = line.split()
        if len(line) < 6:
            raise ValueError("Invalid format")
        if line[0].startswith("d"):
            line_type = "dir"
        else:
            line_type = "file"
        year = datetime.now().strftime("%Y")
        if ":" in line[7]:
            year = datetime.now().strftime("%Y")
            line[7] = f"{line[6]} {line[7]}"
        try:
            line[6] = months[line[6][:3]] + line[6][3:]
            dt = datetime.strptime(f"{line[6]} {year} {line[7]}", "%m %Y %I:%M %p")
        except ValueError:
            raise ValueError("Invalid format")
        size = int(line[4])
        path = " ".join(line[8:])
        return path, {"type": line_type, "size": size, "modify": dt}


    async def get_all_player_atm(self, map_name):
        async with aioftp.Client.context(self.host, port_by_name[map_name], self.user, self.passwd) as client:
            print(f"Connecting to {self.host}:{port_by_name[map_name]} {map_name}  {random.randint(0, 99999)}")
            try:
                for path, info in await client.list():
                    if info["type"] == "file" and path.suffix == ".json":
                        print(path)
            except aioftp.StatusCodeError as e:
                print(f"Error: {e.message}")


    async def get_one_player_atm(self, map_name, SK64):
        pass