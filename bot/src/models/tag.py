from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Tag",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.tag import Tag as TagData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Tag:
    TABLE: ClassVar[str] = "tags"
    id: int
    name: str
    owner_id: int
    message: str
    use_condition: str

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TagData) -> Tag:
        ...

    def to_dict(self) -> TagData:
        ...

    def update(self, data: Tag) -> Tag:
        ...
