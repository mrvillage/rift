from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Alliance",)

if TYPE_CHECKING:
    import decimal
    from typing import ClassVar

    from pnwkit.data import Alliance as PnWKitAlliance

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

    def to_dict(self) -> AllianceData:
        ...

    @classmethod
    def from_data(cls, data: PnWKitAlliance) -> Alliance:
        if TYPE_CHECKING:
            assert isinstance(data.score, decimal.Decimal)
        return cls(
            id=int(data.id),
            name=data.name,
            acronym=data.acronym,
            score=data.score,
            color=getattr(enums.Color, data.color.upper()),
            date=datetime.datetime.fromisoformat(data.date),
            accepts_members=data.acceptmem,
            flag=data.flag,
            forum_link=data.forumlink,
            discord=data.irclink,
            estimated_resources=models.Resources(),
        )
