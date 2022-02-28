from __future__ import annotations

from ..bot import bot
from .common import CommonSlashCommand

__all__ = ("AdminCommand",)


@bot.command
class AdminCommand(
    CommonSlashCommand, name="admin", description="Super secret, don't touch."
):
    ...
