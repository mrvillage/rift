from __future__ import annotations

from typing import TYPE_CHECKING

from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()

if TYPE_CHECKING:

    class AllianceSettingsCommandOptions:
        ...


@bot.command
class AllianceSettingsCommand(
    CommonSlashCommand["AllianceSettingsCommandOptions"],
    name="alliance-settings",
    description=".",
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
