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
    "menu_layout",
    "menu_created",
    "menu_edited",
    "menu_list",
    "menu_item_action_added_roles",
    "menu_item_action_removed_roles",
    "menu_item_action_toggled_roles",
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
    return strings.model_created_id("Menu item", item.id)


def menu_item_deleted(item: models.MenuItem) -> str:
    return strings.model_deleted_id("Menu item", item.id)


def menu_item_edited(item: models.MenuItem) -> str:
    return strings.model_edited_id("Menu item", item.id)


def menu_item_has_no_menu(item: models.MenuItem) -> str:
    return f"Menu item with ID {item.id} has no menu!"


def menu_item_moved(item: models.MenuItem) -> str:
    return f"Menu item with ID {item.id} has been moved!"


def menu_deleted(menu: models.Menu) -> str:
    return strings.model_deleted("Menu", menu)


def menu_sent(menu: models.Menu, channel: quarrel.TextChannel | quarrel.Thread) -> str:
    return f"Menu {menu} sent to <@#{channel.id}>!"


def menu_layout(menu: models.Menu) -> str:
    return f"Showing layout for menu {menu}."


def menu_created(menu: models.Menu) -> str:
    return strings.model_created("Menu", menu)


def menu_edited(menu: models.Menu) -> str:
    return strings.model_edited("Menu", menu)


def menu_list(menu: list[models.Menu]) -> str:
    return strings.model_list("Menu", menu)


def menu_item_action_added_roles(
    roles: list[quarrel.Role],
) -> str:
    return (
        f"Added roles {', '.join(role.mention for role in roles)}!"
        if roles
        else "No roles added!"
    )


def menu_item_action_removed_roles(
    roles: list[quarrel.Role],
) -> str:
    return (
        f"Removed roles {', '.join(role.mention for role in roles)}!"
        if roles
        else "No roles removed!"
    )


def menu_item_action_toggled_roles(
    added: list[quarrel.Role], removed: list[quarrel.Role]
) -> str:
    return f"{menu_item_action_added_roles(added)}\n{menu_item_action_removed_roles(removed)}"
