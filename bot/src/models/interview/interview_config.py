from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("InterviewConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InterviewConfig:
    TABLE: ClassVar[str] = "interview_configs"
    id: int
    name: str
    guild_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InterviewConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: InterviewConfig) -> InterviewConfig:
        ...
