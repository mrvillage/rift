from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import strings

__all__ = (
    "menu_has_no_space",
    "menu_item_created",
    "menu_item_created",
    "menu_item_deleted",
    "menu_item_edited",
    "menu_item_has_no_menu",
    "menu_item_moved",
    "menu_deleted",
    "menu_sent",
)

if TYPE_CHECKING:
    from quarrel import Missing

    from .. import models


def menu_has_no_space(
    menu: models.Menu, item: models.MenuItem, row: Missing[int], column: Missing[int]
) -> str:
    row_str = f" in row {row}" if row is not quarrel.MISSING else ""
    column_str = (
        f" {'and' if row is not quarrel.MISSING and column is not quarrel.MISSING else 'in'} column {column}"
        if column is not quarrel.MISSING
        else ""
    )
    return f"Menu {menu.name} has no space for that item{row_str}{column_str}!"


def menu_item_created(item: models.MenuItem) -> str:
    return strings.model_created("Menu item", item.id)


def menu_item_deleted(item: models.MenuItem) -> str:
    return strings.model_deleted("Menu item", item.id)


def menu_item_edited(item: models.MenuItem) -> str:
    return strings.model_edited("Menu item", item.id)


def menu_item_has_no_menu(item: models.MenuItem) -> str:
    return f"Menu item with ID {item.id} has no menu!"


def menu_item_moved(item: models.MenuItem) -> str:
    return f"Menu item with ID {item.id} has been moved!"


def menu_deleted(menu: models.Menu) -> str:
    return strings.model_deleted("Menu", menu.id)


def menu_sent(menu: models.Menu, channel: quarrel.TextChannel | quarrel.Thread) -> str:
    return f"Menu {menu} sent to <@#{channel.id}>!"
