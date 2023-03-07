from os import getenv
from colorama import Fore, Style

color_map = {
    "DEBUG": {
        "color": Fore.BLUE,
        "int": 4
        },
    "INFO": {
        "color": Fore.GREEN,
        "int": 3
        },
    "WARNING": {
        "color": Fore.YELLOW,
        "int": 2
        },
    "ERROR":  {
        "color": Fore.RED,
        "int": 1
        },
    "CRITICAL":  {
        "color": Fore.RED + Style.BRIGHT,
        "int": 0
        },
    "COG":  {
        "color": Fore.CYAN,
        "int": 0
        },
    "GUILD":  {
        "color": Fore.CYAN,
        "int": 0
        },
    }



def colorized_print(print_type: str, message: str) -> None:
    """
    Helper function to colorize log output based on level.
    """
    # Set color based on log level
    format = f'{color_map[print_type]["color"]}[{print_type}] {message}{Style.RESET_ALL}'
    if color_map[print_type]["int"] <= int(getenv("APP_LOGGING_LEVEL")):
        print(format)
