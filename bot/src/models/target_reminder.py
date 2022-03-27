from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("TargetReminder",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.target_reminder import TargetReminder as TargetReminderData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetReminder:
    TABLE: ClassVar[str] = "target_reminders"
    id: int
    nation_id: int
    owner_id: int
    mention_ids: list[int]
    direct_message: bool
    times: list[int]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TargetReminderData) -> TargetReminder:
        ...

    def to_dict(self) -> TargetReminderData:
        ...

    def update(self, data: TargetReminder) -> TargetReminder:
        ...
