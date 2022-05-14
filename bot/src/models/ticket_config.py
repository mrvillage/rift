from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("TicketConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


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

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TicketConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: TicketConfig) -> TicketConfig:
        ...
