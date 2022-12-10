import os
import json
import random
import shutil
from string import ascii_lowercase, ascii_uppercase
from xmlrpc.client import boolean

from disnake import Color, Embed

# =========================================================================================================
def generate_map_passkey() -> str:
    """generates a random key to associate with a map to be used for deletion confirmation"""
    passkey = ""
    while len(passkey) < 16:
        rand_int = random.randint(0, 9)
        rand_str = random.choice(ascii_lowercase+ascii_uppercase)
        random_choice = random.choice([rand_int, rand_str])
        passkey += str(random_choice)

    return passkey

# =========================================================================================================
def initial_dir_setup() -> None:
    """called automatically on bot ready, create files required for bot"""
    try:
        os.makedirs(f"_files")
        os.makedirs(f"extra_resources")
        print(f"First Time Startup.")
        print(f"Root Directory Created\n")
    except:
        pass

# =========================================================================================================
def create_new_server_dir(server_id) -> None:
    """called automatically on bot ready, creates required files for server"""

    try:
        os.makedirs(f"_files/{server_id}")
        os.makedirs(f"_files/{server_id}/maps")
        os.makedirs(f"_files/{server_id}/support")
        shutil.copyfile("src/discord/template_files/settings.json", f"_files/{server_id}/support")
        print(f"\t\tDirectories Created.")
    except FileExistsError:
        print(f"\t\tReady.")

# =========================================================================================================
def create_new_map_dir(server_id, map_name) -> bool:
    """Returns True if map directory does not exist"""
    
    passkey = {
        "map_name": map_name, 
        "passkey": generate_map_passkey()
        }

    if map_name not in os.listdir(f"_files/{server_id}/maps"):
        os.makedirs(f"_files/{server_id}/maps/{map_name}")
        os.makedirs(f"_files/{server_id}/maps/{map_name}/inputs")
        os.makedirs(f"_files/{server_id}/maps/{map_name}/outputs")
        os.makedirs(f"_files/{server_id}/maps/{map_name}/atms")
        os.makedirs(f"_files/{server_id}/maps/{map_name}/backups")
        with open(f"_files/{server_id}/maps/{map_name}/passkey.json", "w") as json_out:
            json.dump(passkey, json_out, indent=4)


        return True
    else:
        return False

# =========================================================================================================
def get_map_key(server_id:int, map_name:str) -> str:
    """if map passkey exists return it"""
    path = f"_files/{server_id}/maps/{map_name}/passkey.json"
    try:
        with open(path, "r") as json_in:
            passkey = json.load(json_in)
    except FileNotFoundError:
        print("No map or passkey found.")
        return None
    return passkey

# =========================================================================================================
def remove_map_dir(server_id:int, map_name:str) -> None:
    """Destory the directory given the server_id and map_name"""
    path = f"_files/{server_id}/maps/{map_name}"
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))

# =========================================================================================================
def remove_embed(map_name):
    """return a removal confirmation Embed"""
    embed = Embed(title=map_name, description="Map Removed!\nThis can NOT be undone.", color=Color.green())
    return embed

# =========================================================================================================
def key_embed(map_name:str, passkey:str) -> Embed:
    """returns an Embed containing a map passkey"""
    embed = Embed(title=map_name, description=passkey, color=Color.blurple())
    return embed



# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
if __name__ == "__main__":
    for i in range(25):
        print(generate_map_passkey())
    inputasd = input()
