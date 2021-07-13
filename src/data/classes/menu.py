from __future__ import annotations

from json import dumps, loads
from typing import Any, Mapping, Sequence, Union

from discord import ButtonStyle, Embed, Emoji, PartialEmoji
from discord.ext.commands import FlagConverter
from discord.ext.commands.context import Context

from ... import ui
from ..db import execute_query
from ..query import get_menu
from .base import Defaultable, Fetchable, Initable, Setable


class Menu(Defaultable, Fetchable, Initable, Setable):
    menu_id: str
    items: list[Mapping[str, Union[int, str]]]

    def __init__(self, data: Sequence[Any]) -> None:
        self.default = False
        self.menu_id = data[0]
        self.owner_id = data[1]
        self.description = data[2]
        self.items = loads(data[3]) if data[3] else []
        self.permissions = loads(data[4]) if data[4] else {}

    @classmethod
    async def fetch(cls, menu_id: Union[int, str], owner_id: Union[int, str]) -> Menu:
        try:
            return cls(data=await get_menu(menu_id=menu_id))
        except IndexError:
            return cls.default(menu_id=menu_id, owner_id=owner_id)

    @classmethod
    def default(cls, menu_id: Union[int, str], owner_id: Union[int, str]) -> Menu:
        menu = cls(data=[str(menu_id), str(owner_id), None, None, None])
        menu.default = True
        return menu

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

    def get_view(self) -> ui.View:
        self.view = ui.View(timeout=None)
        for item in self.items:
            if item["type"] == "button":

                class Buttoon(ui.Button):
                    async def callback(self, interaction):
                        print("hi")

                button = Buttoon(
                    style=ButtonStyle[item["style"]],
                    label=item["label"],
                    disabled=item["disabled"],
                    custom_id=item["id"],
                    url=item["url"],
                    emoji=item["emoji"],
                    row=item["row"],
                )
                self.view.add_item(button)
            else:
                select = ui.Select(
                    custom_id=item["custom_id"],
                    placeholder=item["placeholder"],
                    min_values=item["min_values"],
                    max_values=item["max_values"],
                    options=[
                        ui.SelectOption(
                            label=option["label"],
                            description=option["description"],
                            emoji=option["emoji"],
                            default=option["default"],
                        )
                        for option in item["options"]
                    ],
                    row=item["row"],
                )
                self.view.add_item(select)
        return self.view

    def get_description_embed(self, ctx: Context) -> Embed:
        from ...funcs import get_embed_author_guild

        self.embed = get_embed_author_guild(ctx.guild, self.description)
        return self.embed
