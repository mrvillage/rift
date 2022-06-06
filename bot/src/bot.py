from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from . import env

__all__ = ("Bot", "bot")

if TYPE_CHECKING:
    from .tasks.common import CommonTask


class Bot(quarrel.Bot):
    running_tasks: list[CommonTask]
    __slots__ = ("running_tasks",)


intents = quarrel.Intents(guilds=True, members=True)
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


@bot.event
async def on_ready() -> None:
    print("Ready!", flush=True)
