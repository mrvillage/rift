from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Roster",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Roster:
    TABLE: ClassVar[str] = "rosters"
    id: int
    nation_id: int
    alliance_id: int
    join_date: datetime.datetime
    time_zone: decimal.Decimal

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Roster:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Roster) -> Roster:
        ...
