from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Treaty",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from pnwkit.data import Treaty as PnWKitTreaty

    from ...types.models.pnw.treaty import Treaty as TreatyData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Treaty:
    TABLE: ClassVar[str] = "treaties"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("type",)
    id: int
    date: datetime.datetime
    type: enums.TreatyType
    url: str
    turns_left: int
    sender_id: int
    receiver_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TreatyData) -> Treaty:
        ...

    def to_dict(self) -> TreatyData:
        ...

    def update(self, data: Treaty) -> Treaty:
        ...

    @classmethod
    def from_data(cls, data: PnWKitTreaty) -> Treaty:
        return cls(
            id=data.id,
            date=data.date,
            type=getattr(enums.TreatyType, data.treaty_type.upper()),
            url=data.treaty_url,
            turns_left=data.turns_left,
            sender_id=data.alliance1_id,
            receiver_id=data.alliance2_id,
        )
