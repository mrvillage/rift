__version__ = "Beta 0.11.1"

import os

from dotenv import load_dotenv
from pnwkit import set_key

__all__ = (
    "TOKEN",
    "DEBUG_TOKEN",
    "FOOTER",
    "COLOR",
    "PNW_API_KEY",
    "PNW_EMAIL",
    "PNW_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "SOCKET_PORT",
    "SOCKET_IP",
    "APPLICATION_ID",
    "DEBUG_APPLICATION_ID",
    "PNW_BOT_KEY",
)

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
DEBUG = os.getenv("DEBUG") == "true"
PNW_BOT_KEY = str(os.getenv("PNW_BOT_KEY"))

set_key(PNW_API_KEY)

HS_YES_CUSTOM_ID = str(os.getenv("HS_YES_CUSTOM_ID"))
HS_NO_CUSTOM_ID = str(os.getenv("HS_NO_CUSTOM_ID"))
HS_OFFSHORE_ID = int(os.getenv("HS_OFFSHORE_ID"))  # type: ignore
HS_SOLDIER_MMR = int(os.getenv("HS_SOLDIER_MMR"))  # type: ignore
HS_TANK_MMR = int(os.getenv("HS_TANK_MMR"))  # type: ignore
HS_AIRCRAFT_MMR = int(os.getenv("HS_AIRCRAFT_MMR"))  # type: ignore
HS_SHIP_MMR = int(os.getenv("HS_SHIP_MMR"))  # type: ignore
HS_MONEY_REQ = int(os.getenv("HS_MONEY_REQ"))  # type: ignore
HS_FOOD_REQ_START = int(os.getenv("HS_FOOD_REQ_START"))  # type: ignore
HS_FOOD_REQ = int(os.getenv("HS_FOOD_REQ"))  # type: ignore
HS_URANIUM_REQ = int(os.getenv("HS_URANIUM_REQ"))  # type: ignore
HS_STEEL_REQ = int(os.getenv("HS_STEEL_REQ"))  # type: ignore
HS_ALUMINUM_REQ = int(os.getenv("HS_ALUMINUM_REQ"))  # type: ignore
HS_GASOLINE_REQ = int(os.getenv("HS_GASOLINE_REQ"))  # type: ignore
HS_MUNITIONS_REQ = int(os.getenv("HS_MUNITIONS_REQ"))  # type: ignore
HS_SPREADSHEET_ID = str(os.getenv("HS_SPREADSHEET_ID"))
