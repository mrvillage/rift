from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Subscription",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Subscription:
    TABLE: ClassVar[str] = "subscriptions"
    id: int
    guild_id: int
    channel_id: int
    owner_id: int
    event: str
    sub_types: list[str]
    condition: str
    mentions: list[int]

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Subscription:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Subscription) -> Subscription:
        ...
