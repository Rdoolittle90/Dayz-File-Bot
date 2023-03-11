"""
A class for interacting with the CFTools API.

Attributes:
- server_info (dict): A dictionary containing information about the CFTools servers.
- chernarus (str): The name of the Chernarus map.
- takistan (str): The name of the Takistan map.
- namalsk (str): The name of the Namalsk map.
- maps (list): A list containing the names of all maps.

Methods:
- generate_server_id(game_identifier: int, ipv4: str, game_port: int) -> str:
    Generates a unique server ID based on the game identifier, IP address, and game port.
- make_authenticated_request(method: str, url: str, token=None, json=None):
    Makes an authenticated request to the CFTools API.
- authenticate() -> str:
    Authenticates with the CFTools API and returns an access token.
"""

import datetime
import hashlib
import json
from os import getenv

import requests

from src.helpers.colored_printing import colorized_print


class CFTools:
    """A Class for connecting to rhe CFTools API"""
    map_info = {
        "Chernarus": {
            "map_id":getenv("CFTools_Map_1_ID"),
            "server_id": getenv("CFTools_Map_1_Server_ID")
        },
        "Takistan": {
            "map_id":getenv("CFTools_Map_2_ID"),
            "server_id": getenv("CFTools_Map_2_Server_ID")
        },
        "Namalsk": {
            "map_id":getenv("CFTools_Map_3_ID"),
            "server_id": getenv("CFTools_Map_3_Server_ID")
        }
    }
    server_info = {0:{}, 1:{}, 2:{}}

    def __init__(self):
        """
        Initializes a new instance of the CFTools class.
        """
        with open("_files/support/settings.json", "r") as json_in:
            data = json.load(json_in)
        self.token = self.authenticate()
        with open("_files/support/settings.json", "w") as json_out:
            json.dump(data, json_out, indent=4)
        self.utc_then = datetime.datetime.utcnow()
        colorized_print("DEBUG", "CFTools has been initialized")


    def generate_server_id(self, game_identifier: int, ipv4: str, game_port: int) -> str:
        """
        Generates a unique server ID based on the game identifier, IP address, and game port.

        Args:
        - game_identifier (int): The game identifier.
        - ipv4 (str): The IP address of the server.
        - game_port (int): The game port of the server.

        Returns:
        - A string representing the unique server ID.
        """
        server_string = f"{game_identifier}{ipv4}{game_port}"
        hash_object = hashlib.sha1(server_string.encode())
        hex_digest = hash_object.hexdigest()
        return hex_digest


    def make_authenticated_request(self, method: str, url: str, token=None, params=None):
        """
        Makes an authenticated request to the CFTools API.

        Args:
        - method (str): The HTTP method to use.
        - url (str): The URL to request.
        - token (str): An optional access token to use for authentication.
        - json (dict): An optional JSON payload to include with the request.

        Returns:
        - The response from the API.

        Raises:
        - requests.exceptions.HTTPError: If the request fails.
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        colorized_print("DEBUG", f"Making {method} request to {url}")
        response = requests.request(method, url, headers=headers, params=params, timeout=10)
        if response.status_code == 403 and response.json().get("error") in ["expired-token", "bad-token"]:
            colorized_print("WARNING", "Token expired, authenticating again...")
            self.token = self.authenticate()
            headers["Authorization"] = f"Bearer {self.token}"
            colorized_print("DEBUG", f"Making {method} request to {url}")
            response = requests.request(method, url, headers=headers, params=params, timeout=10)
            colorized_print("DEBUG", f"Response status code: {response.status_code}")
            response.raise_for_status()
        else:
            colorized_print("DEBUG", f"Response status code: {response.status_code}")
        return response

    def authenticate(self) -> str:
        """
        Authenticates with the CFTools API and returns an access token.

        Returns:
        - A string representing the access token.
        """
        auth_url = "https://data.cftools.cloud/v1/auth/register"
        payload = {"application_id": getenv("CFTools_App_ID"), "secret": getenv("CFTools_secret")}
        colorized_print("DEBUG", "Authenticating with CFTools API...")
        response = requests.post(auth_url, json=payload, timeout=10)
        colorized_print("DEBUG", f"Response status code: {response.status_code}")
        response.raise_for_status()
        colorized_print("DEBUG", "Authentication successful!")
        self.token = response.json()["token"]
        self.set_token(self.token)


    def get_settings(self):
        with open("_files/support/settings.json", "r") as json_in:
            settings = json.load(json_in)
        return settings
    

    def set_token(self, token):
        settings = self.get_settings()
        settings["CFTools_AUTH"] = token
        with open("_files/support/settings.json", "w") as json_out:
            settings = json.dump(settings, json_out, indent=4)
    

    def read_leaderboard_info(self, map=None, stat="kdratio", limit=15):
        map_data = {}

        if map is not None:
            map_names = [map]
        else:
            map_names = CFTools.map_info.keys()

        for map_name in map_names:
            map_data[map_name] = []
            with open(f"_files/maps/{map_name}/data/{stat}_{limit}.json") as file:
                data = json.load(file)
            file_date = datetime.datetime.strptime(data["collected_at"], '%Y-%m-%d %H:%M:%S.%f')
            now = datetime.datetime.now()
            time_difference = (file_date - now).total_seconds()

            if time_difference > 300:
                return None

            player_stats = {}
            for player in data['leaderboard']:
                cftools_id = player['cftools_id']
                name = player['latest_name']
                kills = player.get('kills', 0)
                deaths = (
                    player.get('deaths', 0) +
                    player.get('environment_deaths', 0) +
                    player.get('falldamage_deaths', 0) +
                    player.get('infected_deaths', 0) +
                    player.get('suicides', 0)
                )
                player_stats[cftools_id] = {
                    'name': name,
                    'kills': kills,
                    'deaths': deaths
                }

            leaderboard_ordering_list = [(
                    stats["name"],
                    stats['kills'],
                    stats['deaths'],
                    round(float(stats['kills'] / stats['deaths'] if stats['deaths'] != 0 else stats['kills']), 1)
                )
                for stats in player_stats.values()
                if stats['deaths'] != 0 and stats['kills'] > 0 and stats['kills'] / stats['deaths'] >= 0.1
            ]

            map_data[map_name] = sorted(leaderboard_ordering_list, key=lambda x: x[3], reverse=True)
        return map_data


    def get_leaderboard_info(self, map=None, stat="kdratio", order=-1, limit=100):
        leaderboard_payload = {"stat": stat, "order": order, "limit": limit}

        if map is not None:
            map_names = [map]
        else:
            map_names = CFTools.map_info.keys()

        for map_name in map_names:
            info = CFTools.map_info[map_name]
            response = self.make_authenticated_request("GET", f'https://data.cftools.cloud/v1/server/{info["server_id"]}/leaderboard', token=self.token, params=leaderboard_payload)
            data = response.json()
            data["collected_at"] = str(datetime.datetime.now())
            with open(f"_files/maps/{map_name}/data/{leaderboard_payload['stat']}_{leaderboard_payload['limit']}.json", "w", encoding="utf-8") as json_out:
                json.dump(data, json_out, indent=4)