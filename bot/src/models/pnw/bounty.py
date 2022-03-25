from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Bounty",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from ...types.models.pnw.bounty import Bounty as BountyData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Bounty:
    TABLE: ClassVar[str] = "bounties"
    id: int
    date: datetime.datetime
    nation_id: int
    amount: int
    type: enums.BountyType = attrs.field(converter=enums.BountyType)

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: BountyData) -> Bounty:
        ...
