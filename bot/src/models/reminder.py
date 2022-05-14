from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Reminder",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Reminder:
    TABLE: ClassVar[str] = "reminders"
    id: int
    name: str
    message: str
    owner_id: int
    mention_ids: list[int]
    direct_message: bool
    date: datetime.datetime
    interval: datetime.timedelta

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Reminder:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Reminder) -> Reminder:
        ...
