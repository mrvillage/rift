from __future__ import annotations

import decimal

import quarrel

from .common import CommonOption

__all__ = (
    "DECIMAL_AMOUNT",
    "DECIMAL_AMOUNT_REQUIRED",
    "POSITIVE_DECIMAL_AMOUNT_REQUIRED",
    "FLOAT_AMOUNT",
    "FLOAT_AMOUNT_REQUIRED",
    "INTEGER_AMOUNT",
    "INTEGER_AMOUNT_REQUIRED",
    "PAGE",
)


DECIMAL_AMOUNT = CommonOption(
    type=quarrel.ApplicationCommandOptionType.NUMBER,
    name="amount",
    description="The amount to use.",
    converter=lambda command, value: decimal.Decimal(round(value, 2)),
    default=lambda command: quarrel.MISSING,
)
DECIMAL_AMOUNT_REQUIRED = CommonOption(
    type=quarrel.ApplicationCommandOptionType.NUMBER,
    name="amount",
    description="The amount to use.",
    converter=lambda command, value: decimal.Decimal(round(value, 2)),
)
POSITIVE_DECIMAL_AMOUNT_REQUIRED = CommonOption(
    type=quarrel.ApplicationCommandOptionType.NUMBER,
    name="amount",
    description="The amount to use.",
    converter=lambda command, value: decimal.Decimal(round(value, 2)),
    min_value=0,
)
FLOAT_AMOUNT = CommonOption(
    type=quarrel.ApplicationCommandOptionType.NUMBER,
    name="amount",
    description="The amount to use.",
    default=lambda command: quarrel.MISSING,
)
FLOAT_AMOUNT_REQUIRED = CommonOption(
    type=quarrel.ApplicationCommandOptionType.NUMBER,
    name="amount",
    description="The amount to use.",
)
INTEGER_AMOUNT = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="amount",
    description="The amount to use.",
    default=lambda command: quarrel.MISSING,
)
INTEGER_AMOUNT_REQUIRED = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="amount",
    description="The amount to use.",
)

PAGE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="page",
    description="The page to view.",
    default=1,
    min_value=1,
)
