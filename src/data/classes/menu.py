from __future__ import annotations

from json import dumps, loads
from typing import Any, Mapping, Sequence, Union

from discord import Embed, Message
from discord.ext.commands import Context

from ... import ui
from ..db import execute_query
from ..query import get_menu, get_menu_item, insert_interface
from .base import Defaultable, Fetchable, Initable, Makeable, Saveable, Setable


class Menu(Defaultable, Fetchable, Initable, Makeable, Saveable, Setable):
    menu_id: str
    items: list[Mapping[str, Union[int, str]]]

    def __init__(self, *, data: Sequence[Any]) -> None:
        self.default = False
        self.menu_id = data[0]
        self.owner_id = data[1]
        self.name = data[2]
        self.description = data[3]
        self.item_ids = loads(data[4])
        self.permissions = loads(data[5]) if data[5] else {}

    @classmethod
    async def convert(cls, ctx: Context, argument):
        return await cls.fetch(int(argument), ctx.author.id)

    @classmethod
    async def fetch(cls, menu_id: int, owner_id: int) -> Menu:
        try:
            return cls(data=await get_menu(menu_id=menu_id))
        except IndexError:
            return cls.default(menu_id=menu_id, owner_id=owner_id)

    @classmethod
    def default(cls, menu_id: int, owner_id: int) -> Menu:
        menu = cls(data=[menu_id, owner_id, None, None, None])
        menu.default = True
        return menu

    async def _make_items(self) -> None:
        self.items = [await MenuItem.fetch(i) for i in self.item_ids]

    async def set_(self, **kwargs: Mapping[str, Any]) -> Menu:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        if self.default:
            await execute_query(
                f"""
            INSERT INTO menus (menu_id, {', '.join(kwargs.keys())}) VALUES ({', '.join(f'${i}' for i in range(1, len(kwargs)+2))});
            """,
                str(self.menu_id),
                *tuple(kwargs.values()),
            )
        else:
            await execute_query(
                f"""
            UPDATE menu_id SET {sets} WHERE guild_id = $1;
            """,
                str(self.guild_id),
                *args,
            )
        return self

    async def save(self) -> Menu:
        if self.default:
            await execute_query(
                f"""
            INSERT INTO menus (menu_id, owner_id, items, permissions) VALUES ($1, $2, $3, $4);
            """,
                self.menu_id,
                self.owner_id,
                dumps(self.items) if self.items else None,
                dumps(self.permissions) if self.permissions else None,
            )
        else:
            await execute_query(
                f"""
            UPDATE menu_id SET menu_id = $1,
            owner_id = $2,
            items = $3,
            permissions = $4
            WHERE menu_id = $1;
            """,
                self.menu_id,
                self.owner_id,
                dumps(self.items) if self.items else None,
                dumps(self.permissions) if self.permissions else None,
            )
        return self

    def add_item(self, item: Mapping[str, Union[int, str]]) -> None:
        self.items.append(item)

    def remove_item(self, item_id: str) -> None:
        self.items = [i for i in self.items if i["id"] != item_id]

    async def get_view(self) -> ui.View:
        await self.make_attrs("items")
        self.view = ui.View(timeout=None)
        for item in self.item_ids:
            self.view.add_item(item.get_item())
        return self.view

    def get_description_embed(self, ctx: Context) -> Embed:
        from ...funcs import get_embed_author_guild

        self.embed = get_embed_author_guild(ctx.guild, self.description)
        return self.embed

    async def new_interface(self, *, message: Message) -> None:
        await insert_interface(menu_id=self.menu_id, message=message)

    def __str__(self) -> str:
        if self.name is None:
            return f"{self.id}"
        return f"{self.id} - {self.name}"


class MenuItem(Fetchable, Initable, Saveable, Setable):
    def __init__(self, *, data: Mapping[str, Any]) -> None:
        self.item_id = data[0]
        self.owner_id = data[1]
        self.type = data[2]
        self.data = data[3]

    @classmethod
    async def fetch(cls, item_id: int) -> MenuItem:
        return cls(data=await get_menu_item(item_id=item_id))

    def get_item(self, menu_id: int) -> Union[ui.Button, ui.Select]:
        custom_id = f"{menu_id}-{self.item_id}"
        if self.type == "button":
            return ui.Button(
                style=ui.ButtonStyle[self.data["style"]],
                label=self.data["label"],
                disabled=self.data["disabled"],
                custom_id=custom_id,
                url=self.data["url"],
                emoji=self.data["emoji"],
                row=self.data["row"],
            )
        elif self.type == "select":
            return ui.Select(
                custom_id=custom_id,
                placeholder=self.data["placeholder"],
                min_values=self.data["min_values"],
                max_values=self.data["max_values"],
                options=[
                    ui.SelectOption(
                        label=option["label"],
                        description=option["description"],
                        emoji=option["emoji"],
                        default=option["default"],
                    )
                    for option in self.data["options"]
                ],
                row=self.data["row"],
            )
