from __future__ import annotations

import quarrel

from .. import enums, models, strings, utils
from .common import CommonOption

__all__ = (
    "TICKET",
    "TICKET_OPTIONAL",
    "TICKET_DEFAULT_CURRENT",
    "TICKET_CONFIG",
    "TICKET_CONFIG_OPTIONAL",
    "TICKET_CONFIG_DEFAULT_DEFAULT",
    "ARCHIVE_CATEGORY",
    "ARCHIVE_CATEGORY_OPTIONAL",
    "ARCHIVE_CATEGORY_DEFAULT_NONE",
    "NAME_FORMAT",
    "NAME_FORMAT_OPTIONAL",
    "CLOSE_ACTION",
    "CLOSE_ACTION_OPTIONAL",
)

TICKET = CommonOption(
    type=quarrel.ApplicationCommandOptionType.CHANNEL,
    name="ticket",
    description="The ticket to use.",
    converter=models.Ticket.convert,
    channel_types=[quarrel.ChannelType.GUILD_TEXT],
)
TICKET_OPTIONAL = TICKET(default=utils.default_missing)
TICKET_DEFAULT_CURRENT = TICKET(default=utils.default_current_ticket)
TICKET_CONFIG = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="config",
    description="The ticket config to use.",
    converter=models.TicketConfig.convert,
)
TICKET_CONFIG_OPTIONAL = TICKET(default=utils.default_missing)
TICKET_CONFIG_DEFAULT_DEFAULT = TICKET_CONFIG(
    default=utils.default_default_ticket_config,
)
ARCHIVE_CATEGORY = CommonOption(
    type=quarrel.ApplicationCommandOptionType.CHANNEL,
    name="archive-category",
    description="The archive category to use.",
    attribute="archive_category",
    channel_types=[quarrel.ChannelType.GUILD_CATEGORY],
)
ARCHIVE_CATEGORY_OPTIONAL = ARCHIVE_CATEGORY(default=utils.default_missing)
ARCHIVE_CATEGORY_DEFAULT_NONE = ARCHIVE_CATEGORY(default=utils.default_none)
NAME_FORMAT = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="name-format",
    description="The name format to use.",
    attribute="name_format",
)
NAME_FORMAT_OPTIONAL = NAME_FORMAT(default=utils.default_missing)
CLOSE_ACTION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="close-action",
    description="The action to use when closing the ticket.",
    attribute="close_action",
    choices=enums.TicketCloseAction,
)
CLOSE_ACTION_OPTIONAL = CLOSE_ACTION(default=utils.default_missing)
CLOSE_ACTION_DEFAULT = CLOSE_ACTION(default=strings.DEFAULT_TICKET_NAME_FORMAT)
