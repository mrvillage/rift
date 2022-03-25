from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Server",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.server import Server as ServerData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Server:
    TABLE: ClassVar[str] = "servers"
    id: int
    guild_id: int
    name: str
    invite: str
    description: str
    tags: list[str]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: ServerData) -> Server:
        ...
