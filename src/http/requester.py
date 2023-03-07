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
    def __init__(self):
        """
        Initializes a new instance of the CFTools class.
        """
        self.server_info = {0:{}, 1:{}, 2:{}}
        self.map_info = {
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
        with open("_files/support/settings.json", "r") as json_in:
            data = json.load(json_in)


        if data["CFTools_AUTH"] == None:
            self.token = self.authenticate()
            with open("_files/support/settings.json", "w") as json_out:
                data["CFTools_AUTH"] = self.token
                json.dump(data, json_out, indent=4)
                colorized_print("DEBUG", "New token saved to file.")
        else:
            self.token = data["CFTools_AUTH"]
            colorized_print("DEBUG", "Token found in file.")
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


    def make_authenticated_request(self, method: str, url: str, token=None, json=None):
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

        response = requests.request(method, url, headers=headers, json=json, timeout=10)
        if response.status_code == 401 and response.json().get("error") == "expired-token":
            self.token = self.authenticate()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.request(method, url, headers=headers, json=json, timeout=10)
            response.raise_for_status()
        return response


    def authenticate(self) -> str:
        """
        Authenticates with the CFTools API and returns an access token.

        Returns:
        - A string representing the access token.
        """
        auth_url = "https://data.cftools.cloud/v1/auth/register"
        payload = {"application_id": getenv("CFTools_App_ID"), "secret": getenv("CFTools_secret")}
        colorized_print("DEBUG", "Requesting new Auth token")
        response = requests.post(auth_url, json=payload, timeout=10)
        response.raise_for_status()
        colorized_print("DEBUG", "Success new token received")
        return response.json()["token"]
