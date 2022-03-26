from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Roster",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from ..types.models.roster import Roster as RosterData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Roster:
    TABLE: ClassVar[str] = "rosters"
    id: int
    nation_id: int
    alliance_id: int
    join_date: datetime.datetime
    time_zone: decimal.Decimal

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: RosterData) -> Roster:
        ...
