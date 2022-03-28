from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Radiation",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from pnwkit.data import Radiation as PnWKitRadiation

    from ...types.models.pnw.radiation import Radiation as RadiationData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Radiation:
    TABLE: ClassVar[str] = "radiations"
    PRIMARY_KEY: ClassVar[str] = "date"
    date: datetime.datetime
    north_america: decimal.Decimal
    south_america: decimal.Decimal
    europe: decimal.Decimal
    africa: decimal.Decimal
    asia: decimal.Decimal
    australia: decimal.Decimal
    antarctica: decimal.Decimal

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: RadiationData) -> Radiation:
        ...

    def to_dict(self) -> RadiationData:
        ...

    def update(self, data: Radiation) -> Radiation:
        ...

    @classmethod
    def from_data(cls, data: PnWKitRadiation, date: datetime.datetime) -> Radiation:
        if TYPE_CHECKING:
            assert isinstance(data.north_america, decimal.Decimal)
            assert isinstance(data.south_america, decimal.Decimal)
            assert isinstance(data.europe, decimal.Decimal)
            assert isinstance(data.africa, decimal.Decimal)
            assert isinstance(data.asia, decimal.Decimal)
            assert isinstance(data.australia, decimal.Decimal)
            assert isinstance(data.antarctica, decimal.Decimal)
        return cls(
            date=date,
            north_america=data.north_america,
            south_america=data.south_america,
            europe=data.europe,
            africa=data.africa,
            asia=data.asia,
            australia=data.australia,
            antarctica=data.antarctica,
        )

    @property
    def global_(self) -> decimal.Decimal:
        return (
            self.north_america
            + self.south_america
            + self.europe
            + self.africa
            + self.asia
            + self.australia
            + self.antarctica
        ) / 5
