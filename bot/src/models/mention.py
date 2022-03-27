from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("Mention",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.mention import Mention as MentionData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Mention:
    TABLE: ClassVar[str] = "mentions"
    id: int
    owner_id: int
    owner_type: enums.MentionOwnerType
    channel_ids: list[int]
    role_ids: list[int]
    user_ids: list[int]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: MentionData) -> Mention:
        ...

    def to_dict(self) -> MentionData:
        ...
