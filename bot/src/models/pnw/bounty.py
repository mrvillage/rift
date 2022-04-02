from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Bounty",)

if TYPE_CHECKING:
    from typing import ClassVar

    from pnwkit.data import Bounty as PnWKitBounty

    from ...types.models.pnw.bounty import Bounty as BountyData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Bounty:
    TABLE: ClassVar[str] = "bounties"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("type",)
    id: int
    date: datetime.datetime
    nation_id: int
    amount: int
    type: enums.BountyType = attrs.field(converter=enums.BountyType)

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: BountyData) -> Bounty:
        ...

    def to_dict(self) -> BountyData:
        ...

    def update(self, data: Bounty) -> Bounty:
        ...

    @classmethod
    def from_data(cls, data: PnWKitBounty) -> Bounty:
        return cls(
            id=int(data.id),
            date=datetime.datetime.fromisoformat(data.date),
            nation_id=int(data.nation_id),
            amount=data.amount,
            type=getattr(enums.BountyType, data.type),
        )
