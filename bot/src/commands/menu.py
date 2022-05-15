from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import checks, embeds, enums, errors, models, options
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ("MenuCommand",)

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
        item = await models.MenuItem.create(
            menu=self.options.menu,
            type=self.options.type,
            style=self.options.style,
            label=self.options.label,
            disabled=self.options.disabled,
            url=self.options.url,
            emoji=self.options.emoji,
            action=self.options.action,
            action_options=self.options.action_options,
            row=self.options.row,
            column=self.options.column,
        )
        await self.interaction.respond_with_message(
            embed=embeds.menu_item_created(self.interaction, item),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class MenuItemDeleteCommandOptions:
        item: models.MenuItem


class MenuItemDeleteCommand(
    CommonMenuSlashCommand["MenuItemDeleteCommandOptions"],
    name="delete",
    description="Delete a menu item.",
    parent=MenuItemCommand,
    options=[options.MENU_ITEM],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.item.delete()
        await self.interaction.respond_with_message(
            embed=embeds.menu_item_deleted(self.interaction, self.options.item),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class MenuItemEditCommandOptions:
        item: models.MenuItem
        style: quarrel.Missing[enums.MenuItemStyle]
        label: quarrel.Missing[str]
        disabled: quarrel.Missing[bool]
        url: quarrel.Missing[str]
        emoji: quarrel.Missing[int]
        action: quarrel.Missing[enums.MenuItemAction]
        action_options: quarrel.Missing[list[int]]


class MenuItemEditCommand(
    CommonMenuSlashCommand["MenuItemEditCommandOptions"],
    name="edit",
    description="Edit a menu item.",
    parent=MenuItemCommand,
    options=[options.MENU_ITEM, *options.MENU_ITEM_ATTRIBUTES_OPTIONAL_WITHOUT_TYPE],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.item.edit(
            style=self.options.style,
            label=self.options.label,
            disabled=self.options.disabled,
            url=self.options.url,
            emoji=self.options.emoji,
            action=self.options.action,
            action_options=self.options.action_options,
        )
        await self.interaction.respond_with_message(
            embed=embeds.menu_item_edited(self.interaction, self.options.item),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class MenuItemInfoCommandOptions:
        item: models.MenuItem


class MenuItemInfoCommand(
    CommonMenuSlashCommand["MenuItemInfoCommandOptions"],
    name="info",
    description="View information about a menu item.",
    parent=MenuItemCommand,
    options=[options.MENU_ITEM],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_message(
            embed=self.options.item.build_embed(self.interaction),
        )


if TYPE_CHECKING:

    class MenuItemMoveCommandOptions:
        item: models.MenuItem
        row: int
        column: quarrel.Missing[int]


class MenuItemMoveCommand(
    CommonMenuSlashCommand["MenuItemMoveCommandOptions"],
    name="move",
    description="Move a menu item to a different place in the menu.",
    parent=MenuItemCommand,
    options=[
        options.MENU_ITEM,
        options.MENU_ITEM_ROW,
        options.MENU_ITEM_COLUMN_OPTIONAL,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        menu = self.options.item.menu
        if menu is None:
            raise errors.MenuItemHasNoMenuError(self.options.item)
        await menu.move(self.options.item, self.options.row, self.options.column)
        await self.interaction.respond_with_message(
            embed=embeds.menu_item_moved(self.interaction, self.options.item),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class MenuInfoCommandOptions:
        menu: models.Menu


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
