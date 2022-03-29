from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:

    class TootCommandOptions:
        ...


@bot.command
class TootCommand(
    CommonSlashCommand["TootCommandOptions"],
    name="toot",
    description="Toot tooooooot!",
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond(
            quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            content="Toot tooooooot!",
        )
