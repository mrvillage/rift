__version__ = "Alpha 4.0.0"

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("Rift_discord_token")
PATH = f"{os.getcwd()}"
FOOTER = os.getenv("footer")
COLOR = int(os.getenv("color"))
APIKEY = os.getenv("pnw_api_key")
EMAIL = os.getenv("pnw_email")
PASSWORD = os.getenv("pnw_password")
BASEURL = "https://politicsandwar.com/api"
DBHOST = os.getenv("db_host")
DBPORT = os.getenv("db_port")
DBUSER = os.getenv("db_user")
DBPASSWORD = os.getenv("db_password")
DBNAME = os.getenv("db_name")
SOCKET_PORT = os.getenv("socket_port")
SOCKET_IP = os.getenv("socket_ip")
NATION_ID = os.getenv("nation_id")
