from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("EmbassyConfig",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.embassy_config import EmbassyConfig as EmbassyConfigData


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

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: EmbassyConfigData) -> EmbassyConfig:
        ...

    def to_dict(self) -> EmbassyConfigData:
        ...

    def update(self, data: EmbassyConfig) -> EmbassyConfig:
        ...
