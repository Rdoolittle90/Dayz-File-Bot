"""
This module provides functions for managing map directories and generating passkeys.

Functions:
- generate_map_passkey(): 
    Generates a random key to associate with a map for deletion confirmation.
- initial_dir_setup(): 
    Creates directories required for the bot on first-time startup.
- create_new_server_dir(): 
    Creates directories required for the server on bot ready.
- create_new_map_dir(map_name: str) -> bool: 
    Creates a new directory for the given map name and returns True if the directory doesn't exist.
- get_map_key(map_name: str) -> str: 
    Returns the passkey for the given map name.
- remove_map_dir(map_name: str): 
    Deletes the directory for the given map name.
- remove_embed(map_name: str) -> Embed: 
    Returns an Embed confirming the removal of a map.
- key_embed(map_name: str, passkey: str) -> Embed: 
    Returns an Embed containing the passkey for a map.
"""

import os
import json
import random
import shutil
from string import ascii_lowercase, ascii_uppercase

from nextcord import Embed
import nextcord

from src.helpers.colored_printing import colorized_print

# ==================================================================================================


def generate_map_passkey() -> str:
    """generates a random key to associate with a map to be used for deletion confirmation"""
    passkey = ""
    while len(passkey) < 16:
        rand_int = random.randint(0, 9)
        rand_str = random.choice(ascii_lowercase+ascii_uppercase)
        random_choice = random.choice([rand_int, rand_str])
        passkey += str(random_choice)

    return passkey

# ==================================================================================================


def initial_dir_setup() -> None:
    """called automatically on bot ready, create files required for bot"""
    os.makedirs("_files", exist_ok=True)
    os.makedirs("extra_resources", exist_ok=True)

# ==================================================================================================


def create_new_server_dir() -> None:
    """called automatically on bot ready, creates required files for server"""
    dirs_to_create = [
        "_files/",
        "_files/maps",
        "_files/support"
    ]
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
    settings_file = "_files/support/settings.json"
    if not os.path.exists(settings_file):
        template_file = "src/template_files/settings.json"
        if os.path.exists(template_file):
            shutil.copyfile(template_file, settings_file)
        else:
            colorized_print("ERROR", f"Template file {template_file} not found.")

# ==================================================================================================


def create_new_map_dir(map_name) -> bool:
    """Returns True if map directory does not exist"""

    passkey = {
        "map_name": map_name,
        "passkey": generate_map_passkey()
    }

    if map_name not in os.listdir("_files/maps"):
        for dir_name in ["", "inputs", "atms", "backups"]:
            os.makedirs(f"_files/maps/{map_name}/{dir_name}", exist_ok=True)
        with open(f"_files/maps/{map_name}/passkey.json", "w", encoding='utf-8') as json_out:
            json.dump(passkey, json_out, indent=4)

        return True
    else:
        return False

# ==================================================================================================


def get_map_key(map_name: str) -> str:
    """if map passkey exists return it"""
    path = f"_files/maps/{map_name}/passkey.json"
    try:
        with open(path, "r", encoding='utf-8') as json_in:
            passkey = json.load(json_in)
    except FileNotFoundError:
        print("No map or passkey found.")
        return None
    return passkey

# ==================================================================================================


def remove_map_dir(map_name: str) -> None:
    """Destroy the directory given the server_id and map_name"""
    path = f"_files/maps/{map_name}"
    try:
        shutil.rmtree(path)
    except OSError as err:
        print(f"Error: {path} : {err.strerror}")

# ==================================================================================================


def remove_embed(map_name):
    """return a removal confirmation Embed"""
    embed = Embed(
        title=map_name,
        description="Map Removed!\nThis can NOT be undone.",
        color=nextcord.Color.green())
    return embed

# ==================================================================================================


def key_embed(map_name: str, passkey: str) -> Embed:
    """returns an Embed containing a map passkey"""
    embed = Embed(title=map_name, description=passkey,
                  color=nextcord.Color.blurple())
    return embed


# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
if __name__ == "__main__":
    for i in range(25):
        print(generate_map_passkey())
    test_input = input()
