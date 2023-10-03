import random
import string
import pytz

def get_random_token():
    """
    Generate random token
    """
    full = string.digits + string.ascii_letters
    token = ''.join(random.choices(full, k=16))
    return token

def get_tashkent_time(time):
    tashkent_timezone = pytz.timezone('Asia/Tashkent')
    return time.astimezone(tashkent_timezone)