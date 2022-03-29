from __future__ import annotations

from typing import TYPE_CHECKING

from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:

    class AuditCommandOptions:
        ...


@bot.command
class AuditCommand(
    CommonSlashCommand["AuditCommandOptions"],
    name="",
    description=".",
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
