from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import cache, enums, errors, utils

__all__ = ("MenuItem",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from ...commands.common import CommonSlashCommand
    from ...types.models.menu.menu_item import MenuItem as MenuItemData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class MenuItem:
    TABLE: ClassVar[str] = "menu_items"
    id: int
    menu_id: int
    type: enums.MenuItemType = attrs.field(converter=enums.MenuItemType)
    style: enums.MenuItemStyle
    label: str
    disabled: bool
    url: str
    emoji: int
    action: enums.MenuItemAction
    action_options: list[int]

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: MenuItemData) -> MenuItem:
        ...

    def to_dict(self) -> MenuItemData:
        ...

    def update(self, data: MenuItem) -> MenuItem:
        ...

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: int) -> MenuItem:
        item = cache.get_menu_item(value)
        if item is None:
            raise errors.MenuItemNotFoundError(value)
        return item
