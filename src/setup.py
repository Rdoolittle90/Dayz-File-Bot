import os


def initial_dir_setup():
    os.makedirs(f"_files")
    os.makedirs(f"_files/maps")
    os.makedirs(f"extra_resources")

def create_new_map_dir(map_name):
    os.makedirs(f"_files/maps/{map_name}")
    os.makedirs(f"_files/maps/{map_name}/inputs")
    os.makedirs(f"_files/maps/{map_name}/outputs")
    os.makedirs(f"_files/maps/{map_name}/atms")
    os.makedirs(f"_files/maps/{map_name}/backups")
    os.makedirs(f"_files/maps/{map_name}/support")