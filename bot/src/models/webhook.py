from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Webhook",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Webhook:
    TABLE: ClassVar[str] = "webhooks"
    id: int
    channel_id: int
    guild_id: int
    token: str

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Webhook:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Webhook) -> Webhook:
        ...
