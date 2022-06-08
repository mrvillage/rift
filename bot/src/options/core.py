from __future__ import annotations

import decimal

import quarrel

from .. import utils
from .common import CommonOption

__all__ = (
    "DECIMAL_AMOUNT",
    "POSITIVE_DECIMAL_AMOUNT",
    "FLOAT_AMOUNT",
    "INTEGER_AMOUNT",
    "PAGE",
    "TEXT_CHANNEL",
    "USER",
    "USER_OPTIONAL",
    "USER_DEFAULT_SELF",
    "NAME",
    "NAME_OPTIONAL",
    "PUBLIC",
    "PUBLIC_OPTIONAL",
    "PUBLIC_DEFAULT_TRUE",
    "PUBLIC_DEFAULT_FALSE",
    "CATEGORY",
    "CATEGORY_OPTIONAL",
    "DEFAULT_BOOL",
    "DEFAULT_BOOL_OPTIONAL",
)


INTEGER_AMOUNT = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="amount",
    description="The amount to use.",
)
FLOAT_AMOUNT = INTEGER_AMOUNT(type=quarrel.ApplicationCommandOptionType.NUMBER)
DECIMAL_AMOUNT = FLOAT_AMOUNT(
    converter=lambda command, value: decimal.Decimal(round(value, 2))
)
POSITIVE_DECIMAL_AMOUNT = DECIMAL_AMOUNT(min_value=0)

PAGE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="page",
    description="The page to view.",
    default=1,
    min_value=1,
)

TEXT_CHANNEL = CommonOption(
    type=quarrel.ApplicationCommandOptionType.CHANNEL,
    name="channel",
    description="The channel to use.",
    channel_types=[
        quarrel.ChannelType.GUILD_TEXT,
        quarrel.ChannelType.GUILD_NEWS,
        quarrel.ChannelType.GUILD_NEWS_THREAD,
        quarrel.ChannelType.GUILD_PRIVATE_THREAD,
        quarrel.ChannelType.GUILD_PUBLIC_THREAD,
    ],
)
USER = CommonOption(
    type=quarrel.ApplicationCommandOptionType.USER,
    name="user",
    description="The user to use.",
)
USER_OPTIONAL = USER(default=utils.default_missing)
USER_DEFAULT_SELF = USER(default=lambda command: command.interaction.user)
NAME = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="name",
    description="The name to use.",
)
NAME_OPTIONAL = NAME(default=utils.default_missing)
PUBLIC = CommonOption(
    type=quarrel.ApplicationCommandOptionType.BOOLEAN,
    name="public",
    description="Whether it should be public or not.",
)
PUBLIC_OPTIONAL = PUBLIC(default=utils.default_missing)
PUBLIC_DEFAULT_TRUE = PUBLIC(default=True)
PUBLIC_DEFAULT_FALSE = PUBLIC(default=False)
CATEGORY = CommonOption(
    type=quarrel.ApplicationCommandOptionType.CHANNEL,
    name="category",
    description="The category to use.",
    channel_types=[quarrel.ChannelType.GUILD_CATEGORY],
)
CATEGORY_OPTIONAL = CATEGORY(default=utils.default_missing)
DEFAULT_BOOL = CommonOption(
    type=quarrel.ApplicationCommandOptionType.BOOLEAN,
    name="default",
    description="Whether this should be the default or not.",
)
DEFAULT_BOOL_OPTIONAL = DEFAULT_BOOL(default=utils.default_missing)
