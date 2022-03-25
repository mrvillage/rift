from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Treaty",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from ...types.models.pnw.treaty import Treaty as TreatyData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Treaty:
    TABLE: ClassVar[str] = "treaties"
    id: int
    date: datetime.datetime
    type: enums.TreatyType
    turns_left: int
    sender_id: int
    receiver_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TreatyData) -> Treaty:
        ...
