from __future__ import annotations

import decimal
import os

import pnwkit

__all__ = (
    "ENVIRONMENT",
    "PROD_APPLICATION_ID",
    "PROD_TOKEN",
    "BETA_APPLICATION_ID",
    "BETA_TOKEN",
    "DEV_APPLICATION_ID",
    "DEV_TOKEN",
)

ENVIRONMENT = os.environ["ENVIRONMENT"]
PROD_APPLICATION_ID = int(os.environ["PROD_APPLICATION_ID"])
PROD_TOKEN = os.environ["PROD_TOKEN"]
BETA_APPLICATION_ID = int(os.environ["BETA_APPLICATION_ID"])
BETA_TOKEN = os.environ["BETA_TOKEN"]
DEV_APPLICATION_ID = int(os.environ["DEV_APPLICATION_ID"])
DEV_TOKEN = os.environ["DEV_TOKEN"]
DEV_GUILD_IDS = {int(i) for i in os.environ["DEV_GUILD_IDS"].split(",")}
VERIFIED_BOT_KEY = os.environ["VERIFIED_BOT_KEY"]
PNW_API_KEY = os.environ["PNW_API_KEY"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

kit = pnwkit.QueryKit(
    api_key=PNW_API_KEY,
    bot_key=VERIFIED_BOT_KEY,
    bot_key_api_key=PNW_API_KEY,
    parse_float=decimal.Decimal,
)
