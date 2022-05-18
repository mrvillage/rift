from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("EmbassyConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class EmbassyConfig:
    TABLE: ClassVar[str] = "embassy_configs"
    id: int
    name: str
    category_id: int
    guild_id: int
    message: str
    archive_category_id: int
    mentions: list[int]
    default: bool
    name_format: str
    access_level: enums.AccessLevel

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmbassyConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: EmbassyConfig) -> EmbassyConfig:
        ...
