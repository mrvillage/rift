from __future__ import annotations

import os
from typing import TYPE_CHECKING

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
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "DB_NAME": "postgres",
    }
