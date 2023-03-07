import logging
from colorama import Fore, Style


def colorize_log(level: str, message: str) -> None:
    """
    Helper function to colorize log output based on level.
    """
    color_map = {
        "DEBUG": {
            "color": Fore.BLUE,
            "level": logging.DEBUG
            },
        "INFO": {
            "color": Fore.GREEN,
            "level": logging.INFO
            },
        "WARNING": {
            "color": Fore.YELLOW,
            "level": logging.WARNING
            },
        "ERROR":  {
            "color": Fore.RED,
            "level": logging.ERROR
            },
        "CRITICAL":  {
            "color": Fore.RED + Style.BRIGHT,
            "level": logging.CRITICAL
            },
    }

    # Set color based on log level
    color = color_map[level]["color"]

    # Create logger and formatter
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(f'{color}[%(levelname)s] %(message)s{Style.RESET_ALL}')

    # Set level and add formatter to logger
    logger.setLevel(color_map[level]["level"])
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Log message
    getattr(logger, level.lower())(message)

    # Remove handler to reset logger
    logger.removeHandler(handler)