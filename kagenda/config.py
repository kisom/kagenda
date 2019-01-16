import os
import pytz

LOCAL_TZ = pytz.timezone('America/Los_Angeles')
UTC = pytz.utc
OAKLAND = ("37.8380", "-122.2824")


def get_creds_file(name):
    path = os.getenv("KAGENDA_CONFIG", ".")
    return os.path.join(path, name)