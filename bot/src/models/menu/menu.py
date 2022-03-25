from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Menu",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.menu.menu import Menu as MenuData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Menu:
    TABLE: ClassVar[str] = "menus"
    id: int
    guild_id: int
    name: str
    description: str

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: MenuData) -> Menu:
        ...
