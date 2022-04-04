from __future__ import annotations

import decimal

import quarrel

from .common import CommonOption

__all__ = (
    "DECIMAL_AMOUNT",
    "POSITIVE_DECIMAL_AMOUNT",
    "FLOAT_AMOUNT",
    "INTEGER_AMOUNT",
    "PAGE",
    "TEXT_CHANNEL",
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
