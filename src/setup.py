import os
import json
import random
from string import ascii_lowercase, ascii_uppercase
from xmlrpc.client import boolean


def generate_map_passkey() -> str:
    """generates a random key to associate with a map to be used for deletion confirmation"""
    passkey = ""
    while len(passkey) < 16:
        rand_int = random.randint(0, 9)
        rand_str = random.choice(ascii_lowercase+ascii_uppercase)
        random_choice = random.choice([rand_int, rand_str])
        passkey += str(random_choice)

    return passkey


def initial_dir_setup():
    os.makedirs(f"_files")
    os.makedirs(f"_files/maps")
    os.makedirs(f"extra_resources")


def create_new_map_dir(map_name) -> bool:
    """Returns True if map directory does not exist"""
    
    passkey = {
        "map_name": map_name, 
        "passkey": generate_map_passkey()
        }

    if map_name not in os.listdir("_files/maps"):
        os.makedirs(f"_files/maps/{map_name}")
        os.makedirs(f"_files/maps/{map_name}/inputs")
        os.makedirs(f"_files/maps/{map_name}/outputs")
        os.makedirs(f"_files/maps/{map_name}/atms")
        os.makedirs(f"_files/maps/{map_name}/backups")
        os.makedirs(f"_files/maps/{map_name}/support")

        with open(f"_files/maps/{map_name}/passkey.json", "w") as json_out:
            json.dump(passkey, json_out, indent=4)

        return True
    else:
        return False



if __name__ == "__main__":
    for i in range(25):
        print(generate_map_passkey())
    inputasd = input()