from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING

import attrs
import quarrel

from ... import cache, components, consts, embeds, errors, models, utils

__all__ = ("Menu",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from quarrel import Missing

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

    async def save(self, insert: bool = False) -> None:
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

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    @property
    def interfaces(self) -> set[models.MenuInterface]:
        return {i for i in cache.menu_interfaces if i.menu_id == self.id}

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Menu:
        with contextlib.suppress(ValueError):
            menu = cache.get_menu(utils.convert_int(value))
            if menu is not None:
                return menu
        raise errors.MenuNotFoundError(command.interaction, value)

    @classmethod
    async def create(cls, guild_id: int, name: str, description: str) -> Menu:
        self = cls(
            id=0,
            guild_id=guild_id,
            name=name,
            description=description,
            layout=[
                [0 for _ in range(consts.MAX_ACTION_ROW_WIDTH)]
                for _ in range(consts.MAX_ACTION_ROWS)
            ],
        )
        await self.save(insert=True)
        cache.add_menu(self)
        return self

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.menu(interaction, self)

    def build_interface_embed(self, guild: quarrel.Guild) -> quarrel.Embed:
        return embeds.menu_interface(guild, self)

    def build_interface_grid(self) -> quarrel.Grid:
        return components.MenuInterfaceGrid(self)

    async def edit(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        await self.save()

    async def send(self, channel: quarrel.GuildChannel) -> None:
        message = await channel.create_message(
            embed=self.build_interface_embed(channel.guild),
            grid=self.build_interface_grid(),
        )
        await models.MenuInterface.create(self, message)

    def set_item(
        self,
        item: models.MenuItem,
        row: Missing[int] = quarrel.MISSING,
        column: Missing[int] = quarrel.MISSING,
    ) -> None:
        width = item.width
        if width == 1 and row is not quarrel.MISSING and column is not quarrel.MISSING:
            row -= 1
            column -= 1
            self.layout[row][column] = item.id
        elif row is not quarrel.MISSING:
            row -= 1
            offset = self.layout[row].index(0)
            self.layout[row][offset : offset + width] = [item.id] * (
                width
                if width + offset <= consts.MAX_ACTION_ROW_WIDTH
                else width + offset - consts.MAX_ACTION_ROW_WIDTH
            )
        else:
            for i in self.layout:
                with contextlib.suppress(ValueError):
                    offset = i.index(0)
                    i[offset : offset + width] = [item.id] * (
                        width
                        if width + offset <= consts.MAX_ACTION_ROW_WIDTH
                        else width + offset - consts.MAX_ACTION_ROW_WIDTH
                    )
                    break

    def has_space(self, width: int, row: Missing[int], column: Missing[int]) -> bool:
        if width == 1 and row is not quarrel.MISSING and column is not quarrel.MISSING:
            row -= 1
            column -= 1
            if self.layout[row][column] == 0:
                return True
        elif row is not quarrel.MISSING:
            row -= 1
            if len([i for i in self.layout[row] if i == 0]) >= width:
                return True
        else:
            for i in self.layout:
                if len([j for j in i if j == 0]) >= width:
                    return True
        return False

    async def move(self, item: models.MenuItem, row: int, column: Missing[int]) -> None:
        if not self.has_space(item.width, row, column):
            raise errors.MenuHasNoSpaceError(self, item, row, column)
        for i in self.layout:
            i[:] = [j if j != item.id else 0 for j in i]
        self.set_item(item, row, column)
        await self.save()
        await self.update_interfaces()

    async def update_interfaces(self) -> None:
        await asyncio.gather(*(i.update_interface() for i in self.interfaces))
