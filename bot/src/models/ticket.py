from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Ticket",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.ticket import Ticket as TicketData


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
    archived: bool

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TicketData) -> Ticket:
        ...

    def to_dict(self) -> TicketData:
        ...

    def update(self, data: Ticket) -> Ticket:
        ...
