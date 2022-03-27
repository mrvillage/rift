from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("MenuItem",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.menu.menu_item import MenuItem as MenuItemData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class MenuItem:
    TABLE: ClassVar[str] = "menu_items"
    id: int
    menu_id: int
    type: enums.MenuItemType = attrs.field(converter=enums.MenuItemType)
    style: enums.MenuItemStyle
    row: int
    label: str
    disabled: bool
    url: str
    emoji: int
    action: enums.MenuItemAction

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: MenuItemData) -> MenuItem:
        ...

    def to_dict(self) -> MenuItemData:
        ...
