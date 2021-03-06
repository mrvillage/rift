from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AlliancePrivate",)

if TYPE_CHECKING:
    import decimal
    from typing import Any, ClassVar, Optional

    from pnwkit.data import Alliance as PnWKitAlliance

    from ... import models


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AlliancePrivate:
    TABLE: ClassVar[str] = "alliances_private"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    id: int
    resources: Optional[models.Resources]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlliancePrivate:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AlliancePrivate) -> AlliancePrivate:
        ...

    @classmethod
    def from_data(cls, data: PnWKitAlliance) -> AlliancePrivate:
        if data.money is None:
            return cls(id=data.id, resources=None)
        if TYPE_CHECKING:
            assert isinstance(data.money, decimal.Decimal)
            assert isinstance(data.coal, decimal.Decimal)
            assert isinstance(data.oil, decimal.Decimal)
            assert isinstance(data.uranium, decimal.Decimal)
            assert isinstance(data.iron, decimal.Decimal)
            assert isinstance(data.bauxite, decimal.Decimal)
            assert isinstance(data.lead, decimal.Decimal)
            assert isinstance(data.gasoline, decimal.Decimal)
            assert isinstance(data.munitions, decimal.Decimal)
            assert isinstance(data.steel, decimal.Decimal)
            assert isinstance(data.aluminum, decimal.Decimal)
            assert isinstance(data.food, decimal.Decimal)
        return cls(
            id=int(data.id),
            resources=models.Resources(
                money=data.money,
                coal=data.coal,
                oil=data.oil,
                uranium=data.uranium,
                iron=data.iron,
                bauxite=data.bauxite,
                lead=data.lead,
                gasoline=data.gasoline,
                munitions=data.munitions,
                steel=data.steel,
                aluminum=data.aluminum,
                food=data.food,
            ),
        )
