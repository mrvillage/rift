from __future__ import annotations

import os
from typing import TYPE_CHECKING

from src import cache as cache  # noqa: E402
from src import commands as commands  # noqa: E402
from src import components as components  # noqa: E402
from src import db as db  # noqa: E402
from src.bot import bot as bot  # noqa: E402

__all__ = ("init_test_environment",)

if TYPE_CHECKING:
    ...


def init_test_environment() -> None:
    os.environ |= {
        "ENVIRONMENT": "dev",
        "PROD_APPLICATION_ID": "1",
        "PROD_TOKEN": "abc123",
        "BETA_APPLICATION_ID": "2",
        "BETA_TOKEN": "def456",
        "DEV_APPLICATION_ID": "3",
        "DEV_TOKEN": "ghi789",
        "DEV_GUILD_IDS": "1,2,3",
        "VERIFIED_BOT_KEY": "kjl012",
        "PNW_API_KEY": "mno345",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "DB_NAME": "postgres",
    }
