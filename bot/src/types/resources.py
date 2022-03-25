from __future__ import annotations

import decimal
from typing import TypedDict

__all__ = ("Resources",)


class Resources(TypedDict):
    money: decimal.Decimal
    coal: decimal.Decimal
    oil: decimal.Decimal
    uranium: decimal.Decimal
    iron: decimal.Decimal
    bauxite: decimal.Decimal
    lead: decimal.Decimal
    gasoline: decimal.Decimal
    munitions: decimal.Decimal
    steel: decimal.Decimal
    aluminum: decimal.Decimal
    food: decimal.Decimal
