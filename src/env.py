__version__ = "Alpha 8.4.3"

import os

from dotenv import load_dotenv
from pnwkit import set_key

load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
DEBUG_TOKEN = str(os.getenv("DEBUG_TOKEN"))
FOOTER = str(os.getenv("FOOTER"))
COLOR = int(os.getenv("COLOR"))  # type: ignore
PNW_API_KEY = str(os.getenv("PNW_API_KEY"))
PNW_EMAIL = str(os.getenv("PNW_EMAIL"))
PNW_PASSWORD = str(os.getenv("PNW_PASSWORD"))
DB_HOST = str(os.getenv("DB_HOST"))
DB_PORT = str(os.getenv("DB_PORT"))
DB_USER = str(os.getenv("DB_USER"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_NAME = str(os.getenv("DB_NAME"))
SOCKET_PORT = str(os.getenv("SOCKET_PORT"))
SOCKET_IP = str(os.getenv("SOCKET_IP"))
APPLICATION_ID = int(os.getenv("APPLICATION_ID"))  # type: ignore
DEBUG_APPLICATION_ID = int(os.getenv("DEBUG_APPLICATION_ID"))  # type: ignore

set_key(PNW_API_KEY)
