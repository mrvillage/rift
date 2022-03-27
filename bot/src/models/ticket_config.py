from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("TicketConfig",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.ticket_config import TicketConfig as TicketConfigData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TicketConfig:
    TABLE: ClassVar[str] = "ticket_configs"
    id: int
    name: str
    category_id: int
    guild_id: int
    message: str
    archive_category_id: int
    mention_ids: list[int]
    default: bool
    name_format: str
    interview_config_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TicketConfigData) -> TicketConfig:
        ...

    def to_dict(self) -> TicketConfigData:
        ...
