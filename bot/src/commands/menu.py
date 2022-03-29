from __future__ import annotations

from typing import TYPE_CHECKING

from .. import checks, models
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:

    class MenuCommandOptions:
        ...


@bot.command
class MenuCommand(
    CommonSlashCommand["MenuCommandOptions"],
    name="menu",
    description="Manage menus.",
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemCommandOptions:
        ...


@bot.command
class MenuItemCommand(
    CommonSlashCommand["MenuItemCommandOptions"],
    name="item",
    description="Manage menu items.",
    parent=MenuCommand,
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class MenuItemAddCommandOptions:
        item: models.MenuItem


@bot.command
class MenuItemAddCommand(
    CommonSlashCommand["MenuItemAddCommandOptions"],
    name="",
    description=".",
    # options=[options.MENU_ITEM],
    checks=[checks.guild_only, checks.has_guild_role_permissions(manage_menus=True)],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
