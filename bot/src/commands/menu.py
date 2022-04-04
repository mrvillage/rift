from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import checks, enums, models, options
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()

if TYPE_CHECKING:
    from typing import TypeVar

    T = TypeVar("T")


class CommonMenuSlashCommand(
    CommonSlashCommand[T],
    checks=[checks.guild_only, checks.has_guild_role_permissions(manage_menus=True)],
):
    ...


if TYPE_CHECKING:

    class MenuCommandOptions:
        ...


@bot.command
class MenuCommand(
    CommonMenuSlashCommand["MenuCommandOptions"],
    name="menu",
    description="Manage menus.",
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemCommandOptions:
        ...


@bot.command
class MenuItemCommand(
    CommonMenuSlashCommand["MenuItemCommandOptions"],
    name="item",
    description="Manage menu items.",
    parent=MenuCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemCreateCommandOptions:
        menu: models.Menu
        type: enums.MenuItemType
        style: quarrel.Missing[enums.MenuItemStyle]
        label: quarrel.Missing[str]
        disabled: quarrel.Missing[bool]
        url: quarrel.Missing[str]
        emoji: quarrel.Missing[int]
        action: quarrel.Missing[enums.MenuItemAction]
        action_options: quarrel.Missing[list[int]]
        row: quarrel.Missing[int]
        column: quarrel.Missing[int]


@bot.command
class MenuItemCreateCommand(
    CommonMenuSlashCommand["MenuItemCreateCommandOptions"],
    name="create",
    description="Create a menu item on a menu.",
    parent=MenuItemCommand,
    options=[
        options.MENU,
        *options.MENU_ITEM_ATTRIBUTES,
        options.MENU_ITEM_ROW_OPTIONAL,
        options.MENU_ITEM_COLUMN_OPTIONAL,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemDeleteCommandOptions:
        item: models.MenuItem


@bot.command
class MenuItemDeleteCommand(
    CommonMenuSlashCommand["MenuItemDeleteCommandOptions"],
    name="delete",
    description="Delete a menu item.",
    parent=MenuItemCommand,
    options=[options.MENU_ITEM],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemEditCommandOptions:
        item: models.MenuItem
        type: quarrel.Missing[enums.MenuItemType]
        style: quarrel.Missing[enums.MenuItemStyle]
        label: quarrel.Missing[str]
        disabled: quarrel.Missing[bool]
        url: quarrel.Missing[str]
        emoji: quarrel.Missing[int]
        action: quarrel.Missing[enums.MenuItemAction]
        action_options: quarrel.Missing[list[int]]


@bot.command
class MenuItemEditCommand(
    CommonMenuSlashCommand["MenuItemEditCommandOptions"],
    name="edit",
    description="Edit a menu item.",
    parent=MenuItemCommand,
    options=[options.MENU_ITEM, *options.MENU_ITEM_ATTRIBUTES_OPTIONAL],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemInfoCommandOptions:
        item: models.MenuItem


@bot.command
class MenuItemInfoCommand(
    CommonMenuSlashCommand["MenuItemInfoCommandOptions"],
    name="info",
    description="View information about a menu item.",
    parent=MenuItemCommand,
    options=[options.MENU_ITEM],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemMoveCommandOptions:
        item: models.MenuItem
        row: quarrel.Missing[int]
        column: quarrel.Missing[int]


@bot.command
class MenuItemMoveCommand(
    CommonMenuSlashCommand["MenuItemMoveCommandOptions"],
    name="move",
    description="Move a menu item to a different place in the menu.",
    parent=MenuItemCommand,
    options=[
        options.MENU_ITEM,
        options.MENU_ITEM_ROW_OPTIONAL,
        options.MENU_ITEM_COLUMN_OPTIONAL,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuInfoCommandOptions:
        menu: models.Menu


@bot.command
class MenuInfoCommand(
    CommonMenuSlashCommand["MenuInfoCommandOptions"],
    name="info",
    description="View information about a menu.",
    parent=MenuCommand,
    options=[options.MENU],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuCreateCommandOptions:
        ...


@bot.command
class MenuCreateCommand(
    CommonMenuSlashCommand["MenuCreateCommandOptions"],
    name="create",
    description="Create a menu.",
    parent=MenuCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        ...  # show a modal to input the menu name and description


if TYPE_CHECKING:

    class MenuEditCommandOptions:
        menu: models.Menu


@bot.command
class MenuEditCommand(
    CommonMenuSlashCommand["MenuEditCommandOptions"],
    name="edit",
    description="Edit a menu.",
    parent=MenuCommand,
    options=[options.MENU],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...  # show a modal to input the menu name and description


if TYPE_CHECKING:

    class MenuSendCommandOptions:
        menu: models.Menu
        channel: quarrel.TextChannel | quarrel.Thread


@bot.command
class MenuSendCommand(
    CommonMenuSlashCommand["MenuSendCommandOptions"],
    name="send",
    description="Send a menu to a channel.",
    parent=MenuCommand,
    options=[options.MENU, options.TEXT_CHANNEL],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuDeleteCommandOptions:
        menu: models.Menu


@bot.command
class MenuDeleteCommand(
    CommonMenuSlashCommand["MenuDeleteCommandOptions"],
    name="delete",
    description="Delete a menu.",
    parent=MenuCommand,
    options=[options.MENU],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
