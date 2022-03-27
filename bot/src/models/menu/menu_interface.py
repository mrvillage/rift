from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("MenuInterface",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.menu.menu_interface import MenuInterface as MenuInterfaceData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class MenuInterface:
    TABLE: ClassVar[str] = "menu_interfaces"
    id: int
    menu_id: int
    message_id: int
    channel_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: MenuInterfaceData) -> MenuInterface:
        ...

    def to_dict(self) -> MenuInterfaceData:
        ...

    def update(self, data: MenuInterface) -> MenuInterface:
        ...
