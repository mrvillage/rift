from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from src.data.classes import Resources

__all__ = ("RevenueDict",)


class RevenueDictOptional(TypedDict, total=False):
    new_player_bonus: float
    trade_bonus: int


class RevenueDict(RevenueDictOptional):
    gross_income: Resources
    net_income: Resources
    upkeep: Resources
    gross_total: Resources
    net_total: Resources
    upkeep_total: Resources
