from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Interview",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Interview:
    TABLE: ClassVar[str] = "interviews"
    id: int
    config_id: int
    owner_id: int
    ticket_id: int
    require_link: bool

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Interview:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Interview) -> Interview:
        ...
