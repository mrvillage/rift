from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Ticket",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Ticket:
    TABLE: ClassVar[str] = "tickets"
    id: int
    ticket_number: int
    config_id: int
    guild_id: int
    channel_id: int
    owner_id: int
    closed: bool

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Ticket:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Ticket) -> Ticket:
        ...
