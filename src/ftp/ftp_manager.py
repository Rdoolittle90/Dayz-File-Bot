import ftplib
import json
import logging
import os
from ftplib import FTP
from typing import Dict

from src.helpers.colored_printing import colorized_print

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
    paths = {
        "killboard": '/profiles/GAREA_Leaderboard/PlayerDB',
        "atm": '/profiles/LBmaster/Data/LBBanking/Players'
    }
    def __init__(self, map_name):
        """Initializes an FTPConnect object with default values for its attributes."""
        self.ftp = FTP()
        self.is_connected = False
        self.map_name = map_name
        self.host: str = os.getenv("FTP_HOST")
        self.user: str = os.getenv("FTP_USER")
        self.port: int = port_by_name[map_name]
        self.passwd: str = os.getenv("FTP_PASS")
        colorized_print("DEBUG", f"FTP Connection to {self.map_name}:{self.port} has been initialized")
        self.login()

    def login(self):
        try:
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.passwd)
            self.is_connected = True
            colorized_print("INFO", f"Successfully Connected to FTP server {self.map_name}:{self.port}")
        except Exception as e:
            colorized_print("ERROR", f"Could not log in to {self.host}:{self.port}")
            raise e

    def logout(self):
        self.ftp.quit()
        colorized_print("WARNING", f"FTP server {self.map_name}:{self.port} has been logged out")
        

    async def upload_file(self, local_path, path_name, file_name):
        """Uploads a file to the FTP server.

        Args:
            local_path (str): The local path to the file to upload.
            remote_filename (str): The filename to use on the FTP server.
        """
        remote_path = FTPConnect.paths[path_name]
        try:
            if not self.is_connected:
                self.login()
            self.ftp.cwd(FTPConnect.paths[path_name])
            with open(local_path, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}/{file_name}', f)
            colorized_print("DEBUG", f"File {remote_path}/{file_name} uploaded successfully to {remote_path}")
        except Exception as e:
            colorized_print("ERROR", f"Could not upload file {local_path} to {remote_path}")
            self.ftp.quit()
            self.is_connected = False
            raise e


    async def download_one_map_file_async(self, path_name, steam_64):
        try:
            if not self.is_connected:
                colorized_print("WARNING", f"Not logged in")
                self.login()
            remote_path = FTPConnect.paths[path_name]
            self.ftp.cwd(remote_path)

            local_path = f"_files/maps/{self.map_name}/killboards/{steam_64}.json"
            with open(local_path, 'wb') as fout:
                def callback(data):
                    fout.write(data)
                self.ftp.retrbinary('RETR ' + f"{remote_path}/{steam_64}.json", callback)
                colorized_print("DEBUG", f"File {path_name}: {steam_64}.json downloaded successfully")
            with open(local_path, "r") as fin:
                json_data = json.load(fin)
                return json_data

        except ftplib.error_perm as e:
            colorized_print("ERROR", f"Could not download files from {remote_path}")
            os.remove(local_path)
            self.ftp.quit()
            self.is_connected = False
            raise e


    async def download_one_map_atm_file_async(self, steam_64):
        try:
            if not self.is_connected:
                colorized_print("WARNING", f"Not logged in")
                self.login()
            remote_path = '/profiles/LBmaster/Data/LBBanking/Players'
            self.ftp.cwd(remote_path)

            local_path = f"_files/maps/{self.map_name}/atms/{steam_64}.json"
            with open(local_path, 'wb') as fout:
                def callback(data):
                    fout.write(data)
                self.ftp.retrbinary('RETR ' + f"{remote_path}/{steam_64}.json", callback)
                colorized_print("DEBUG", f"File {steam_64}.json downloaded successfully")
            with open(local_path, "r") as fin:
                player_atm = json.load(fin)
                colorized_print("DEBUG", f'       Steam ID: {player_atm["steamid"]}')
                colorized_print("DEBUG", f'    Player Name: {player_atm["playername"]}')
                colorized_print("DEBUG", f'  Current Money: {player_atm["currentMoney"]}')
                colorized_print("DEBUG", f'Max Money Bonus: {player_atm["maxMoneyBonus"]}')
                colorized_print("DEBUG", f' Paycheck Bonus: {player_atm["paycheckBonus"]}')
                return player_atm

        except ftplib.error_perm as e:
            colorized_print("ERROR", f"Could not download files from {remote_path}")
            os.remove(local_path)
            self.ftp.quit()
            self.is_connected = False
            raise e

            
    async def download_all_map_atm_files_async(self):
        if not self.is_connected:
            self.login()
        remote_path = '/profiles/LBmaster/Data/LBBanking/Players'
        self.ftp.cwd(remote_path)
        try:
            files = self.ftp.nlst()
            for file in files:
                if not file.endswith(".json"):
                    continue
                local_path = f"_files/maps/{self.map_name}/atms/{file}"
                with open(local_path, 'wb') as fout:
                    def callback(data):
                        fout.write(data)
                    self.ftp.retrbinary('RETR ' + f"{remote_path}/{file}", callback)
                    colorized_print("DEBUG", f"File {remote_path}/{file} downloaded successfully")
        except Exception as e:
            colorized_print("ERROR", f"Could not download files from {remote_path}")
            self.ftp.quit()
            self.is_connected = False
            raise e