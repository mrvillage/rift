from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Radiation",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from ...types.models.pnw.radiation import Radiation as RadiationData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Radiation:
    TABLE: ClassVar[str] = "radiations"
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
