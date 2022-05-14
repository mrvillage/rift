from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Tag",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


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

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Tag:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Tag) -> Tag:
        ...
