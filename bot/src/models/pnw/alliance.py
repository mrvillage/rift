from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Alliance",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from ... import models
    from ...types.models.pnw.alliance import Alliance as AllianceData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Alliance:
    TABLE: ClassVar[str] = "alliances"
    id: int
    name: str
    acronym: str
    score: decimal.Decimal
    color: enums.Color = attrs.field(converter=enums.Color)
    date: datetime.datetime
    accepts_members: bool
    flag: str
    forum_link: str
    discord: str
    estimated_resources: models.Resources

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AllianceData) -> Alliance:
        ...
