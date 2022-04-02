from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("NationPrivate",)

if TYPE_CHECKING:
    import decimal
    from typing import ClassVar, Optional

    from pnwkit.data import Nation as PnWKitNation

    from ... import models
    from ...types.models.pnw.nation_private import NationPrivate as NationPrivateData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class NationPrivate:
    TABLE: ClassVar[str] = "nations_private"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    id: int
    update_tz: Optional[decimal.Decimal]
    spies: Optional[int]
    resources: Optional[models.Resources]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: NationPrivateData) -> NationPrivate:
        ...

    def to_dict(self) -> NationPrivateData:
        ...

    def update(self, data: NationPrivate) -> NationPrivate:
        ...

    @classmethod
    def from_data(cls, data: PnWKitNation) -> NationPrivate:
        if data.money is None:
            return cls(id=int(data.id), resources=None, update_tz=None, spies=None)
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
            assert isinstance(data.update_tz, decimal.Decimal)
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
            update_tz=data.update_tz,
            spies=data.spies,
        )
