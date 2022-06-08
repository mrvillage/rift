from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import errors

__all__ = ("own_ticket_or_has_permissions",)

if TYPE_CHECKING:
    from .. import models
    from ..commands.common import CommonSlashCommand

    class TicketOptions:
        ticket: models.Ticket


@quarrel.check(requires=["ticket"])
async def own_ticket_or_has_permissions(
    command: CommonSlashCommand[TicketOptions],
) -> bool:
    if command.interaction.guild_id is quarrel.MISSING:
        raise errors.GuildOnlyError()
    if TYPE_CHECKING:
        assert isinstance(command.interaction.user, quarrel.Member)
    if command.options.ticket.owner_id == command.interaction.user.id:
        return True
    if command.interaction.user.permissions.manage_guild:
        return True
    raise errors.MissingDiscordPermissionsError({"manage_guild": True})
