from __future__ import annotations

import quarrel

from . import env

__all__ = ("Bot", "bot")


class Bot(quarrel.Bot):
    ...


intents = quarrel.Intents(guild_members=True)
bot = Bot(
    env.PROD_APPLICATION_ID
    if env.ENVIRONMENT == "prod"
    else env.BETA_APPLICATION_ID
    if env.ENVIRONMENT == "beta"
    else env.DEV_APPLICATION_ID,
    env.PROD_TOKEN
    if env.ENVIRONMENT == "prod"
    else env.BETA_TOKEN
    if env.ENVIRONMENT == "beta"
    else env.DEV_TOKEN,
    intents,
)
