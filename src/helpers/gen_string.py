import random
import string


def generate_random_string(length):
    """placeholder"""
    characters = string.digits + string.ascii_letters
    return ''.join(random.choice(characters) for i in range(length))