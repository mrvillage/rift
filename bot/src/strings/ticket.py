from __future__ import annotations

from typing import TYPE_CHECKING

from .. import strings

__all__ = (
    "ticket_config_deleted",
    "ticket_config_created",
    "ticket_config_edited",
    "ticket_config_list",
    "ticket_opened",
    "ticket_closed",
    "TICKET_CONFIG_NO_DEFAULT_ERROR",
    "DEFAULT_TICKET_NAME_FORMAT",
)

if TYPE_CHECKING:
    from typing import Final

    from .. import models


def ticket_config_deleted(config: models.TicketConfig) -> str:
    return strings.model_deleted("Ticket config", config)


def ticket_config_created(config: models.TicketConfig) -> str:
    return strings.model_created("Ticket config", config)


def ticket_config_edited(config: models.TicketConfig) -> str:
    return strings.model_edited("Ticket config", config)


def ticket_config_list(configs: list[models.TicketConfig]) -> str:
    return strings.model_list("Ticket config", configs)


def ticket_opened(ticket: models.Ticket) -> str:
    return f"Ticket #{ticket.ticket_number} opened: {strings.channel_mention_id(ticket.channel_id)}"


def ticket_closed(ticket: models.Ticket) -> str:
    return f"Ticket #{ticket.ticket_number} closed."


TICKET_CONFIG_NO_DEFAULT_ERROR: Final[
    str
] = "I couldn't find a default ticket config for this server! Please select a specific config."
DEFAULT_TICKET_NAME_FORMAT: Final[str] = "ticket-{ticket_number}"
