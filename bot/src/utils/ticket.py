from __future__ import annotations

from typing import TYPE_CHECKING

from .. import cache, errors

__all__ = ("default_default_ticket_config", "default_current_ticket")

if TYPE_CHECKING:
    from typing import Any

    from .. import models
    from ..commands.common import CommonSlashCommand


def default_default_ticket_config(
    command: CommonSlashCommand[Any],
) -> models.TicketConfig:
    try:
        return next(
            i
            for i in cache.ticket_configs
            if i.guild_id == command.interaction.guild_id and i.default
        )
    except StopIteration as e:
        raise errors.TicketConfigNoDefaultError(command.interaction) from e


def default_current_ticket(
    command: CommonSlashCommand[Any],
) -> models.Ticket:
    try:
        return next(
            i for i in cache.tickets if i.channel_id == command.interaction.channel_id
        )
    except StopIteration as e:
        raise errors.TicketNotFoundError(
            command.interaction, command.interaction.user.id
        ) from e
