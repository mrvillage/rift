from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Radiation",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import Any, ClassVar

    from pnwkit.data import Radiation as PnWKitRadiation


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Radiation:
    TABLE: ClassVar[str] = "radiations"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("date",)
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    date: datetime.datetime
    global_: decimal.Decimal
    north_america: decimal.Decimal
    south_america: decimal.Decimal
    europe: decimal.Decimal
    africa: decimal.Decimal
    asia: decimal.Decimal
    australia: decimal.Decimal
    antarctica: decimal.Decimal

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Radiation:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Radiation) -> Radiation:
        ...

    @classmethod
    def from_data(cls, data: PnWKitRadiation, date: datetime.datetime) -> Radiation:
        if TYPE_CHECKING:
            assert isinstance(data.global_, decimal.Decimal)
            assert isinstance(data.north_america, decimal.Decimal)
            assert isinstance(data.south_america, decimal.Decimal)
            assert isinstance(data.europe, decimal.Decimal)
            assert isinstance(data.africa, decimal.Decimal)
            assert isinstance(data.asia, decimal.Decimal)
            assert isinstance(data.australia, decimal.Decimal)
            assert isinstance(data.antarctica, decimal.Decimal)
        return cls(
            date=date,
            global_=data.global_,
            north_america=data.north_america,
            south_america=data.south_america,
            europe=data.europe,
            africa=data.africa,
            asia=data.asia,
            australia=data.australia,
            antarctica=data.antarctica,
        )
