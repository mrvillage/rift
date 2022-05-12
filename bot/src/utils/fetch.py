from __future__ import annotations

import pnwkit

from .. import models
from ..env import kit

__all__ = ("fetch_discord_username",)

FETCH_DISCORD_USERNAME_QUERY = kit.query(
    "nations", {"id": pnwkit.Variable("id", pnwkit.VariableType.INT_ARRAY)}, "discord"
)


async def fetch_discord_username(nation: models.Nation) -> str:
    result = (await FETCH_DISCORD_USERNAME_QUERY.set_variables(id=nation.id)).nations
    if len(result) == 0:
        return ""
    return result[0].discord
