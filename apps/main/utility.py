import random
import string


def get_random_token():
    """
    Generate random token
    """
    full = string.digits + string.ascii_letters
    token = ''.join(random.choices(full, k=16))
    return token
