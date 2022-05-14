from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("GuildSettings",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class GuildSettings:
    TABLE: ClassVar[str] = "guild_settings"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("guild_id",)
    guild_id: int
    purpose: enums.Purpose = attrs.field(converter=enums.Purpose)
    purpose_argument: str
    public: bool
    description: str
    welcome_message: str
    welcome_channels: list[int]
    join_role_ids: list[int]
    verified_role_ids: list[int]
    member_role_ids: list[int]
    verified_nickname_format: str
    enforce_verified_nickname: bool
    welcome_mentions: list[int]

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GuildSettings:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: GuildSettings) -> GuildSettings:
        ...

    @property
    def key(self) -> int:
        return self.guild_id
