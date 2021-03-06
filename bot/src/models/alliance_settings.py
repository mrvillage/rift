from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("AllianceSettings",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AllianceSettings:
    TABLE: ClassVar[str] = "alliance_settings"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("alliance_id",)
    alliance_id: int
    default_raid_condition: str
    default_nuke_condition: str
    default_military_condition: str
    default_attack_raid_condition: str
    default_attack_nuke_condition: str
    default_attack_military_condition: str
    withdraw_channel_ids: list[int]
    require_withdraw_approval: bool
    offshore_id: int
    withdraw_from_offshore: bool

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AllianceSettings:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AllianceSettings) -> AllianceSettings:
        ...
