__version__ = "Alpha 7.0.0"

import os

from dotenv import load_dotenv
from pnwkit import set_key

load_dotenv()

TOKEN = str(os.getenv("Rift_discord_token"))
PATH = f"{os.getcwd()}"
FOOTER = str(os.getenv("footer"))
COLOR = int(os.getenv("color"))
APIKEY = str(os.getenv("pnw_api_key"))
EMAIL = str(os.getenv("pnw_email"))
PASSWORD = str(os.getenv("pnw_password"))
BASEURL = "https://politicsandwar.com/api"
DBHOST = str(os.getenv("db_host"))
DBPORT = str(os.getenv("db_port"))
DBUSER = str(os.getenv("db_user"))
DBPASSWORD = str(os.getenv("db_password"))
DBNAME = str(os.getenv("db_name"))
SOCKET_PORT = str(os.getenv("socket_port"))
SOCKET_IP = str(os.getenv("socket_ip"))
APPLICATION_ID = int(os.getenv("application_id"))

set_key(APIKEY)
