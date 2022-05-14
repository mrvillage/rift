from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Menu",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from ...commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Menu:
    TABLE: ClassVar[str] = "menus"
    id: int
    guild_id: int
    name: str
    description: str
    layout: list[list[int]]

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Menu:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Menu) -> Menu:
        ...

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Menu:
        ...
