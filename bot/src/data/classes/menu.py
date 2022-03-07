from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Union

import discord
from discord.ext import commands

from ...cache import cache
from ...errors import (
    EmbassyConfigNotFoundError,
    MenuItemNotFoundError,
    MenuNotFoundError,
    TicketConfigNotFoundError,
)
from ...funcs.utils import convert_int
from ...ref import RiftContext
from ..db import execute_query, execute_read_query
from .base import Makeable

__all__ = ("Menu", "MenuItem", "MenuInterface")

if TYPE_CHECKING:
    from _typings import MenuData, MenuFormattedFlags, MenuInterfaceData, MenuItemData

    from ...views.menu import MenuButton, MenuSelect, MenuView


class Menu(Makeable):
    id: int
    name: Optional[str]
    description: Optional[str]
    item_ids: List[List[int]]
    permissions: Mapping[str, Any]

    __slots__ = (
        "id",
        "guild_id",
        "name",
        "description",
        "item_ids",
    )

    def __init__(self, data: MenuData) -> None:
        self.id = data.get("id", 0)
        self.guild_id = data["guild"]
        self.name = data["name"]
        self.description = data["description"]
        self.item_ids = data["items"] or [[], [], [], [], []]

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Menu:
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        return await cls.fetch(convert_int(argument), ctx.guild.id)

    @classmethod
    async def fetch(cls, menu_id: int, guild_id: int) -> Menu:
        menu = cache.get_menu(menu_id)
        if menu is None:
            raise MenuNotFoundError(menu_id)
        if menu.guild_id != guild_id:
            raise MenuNotFoundError(menu_id)
        return menu

    @classmethod
    def default(cls, guild_id: int) -> Menu:
        return cls(
            data={
                "id": 0,
                "guild": guild_id,
                "name": None,
                "description": None,
                "items": [[], [], [], [], []],
            }
        )

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE menus SET id = $1, guild = $2, name = $3, description = $4, items = $5 WHERE id = $1;",
                self.id,
                self.guild_id,
                self.name,
                self.description,
                [[i.id for i in row] for row in self.items]
                if self.items
                else [
                    [],
                    [],
                    [],
                    [],
                    [],
                ],
            )
        else:
            id = await execute_read_query(
                "INSERT INTO menus (guild, name, description, items) VALUES ($1, $2, $3, $4) RETURNING id;",
                self.guild_id,
                self.name,
                self.description,
                [[i.id for i in row] for row in self.items]
                if self.items
                else [
                    [],
                    [],
                    [],
                    [],
                    [],
                ],
            )
            self.id = id[0]["id"]
            cache.add_menu(self)

    def add_item(self, item: MenuItem, row: int) -> None:
        self.item_ids[row].append(item.id)

    def remove_item(self, item_id: str) -> None:
        for i in self.items:
            for j in i:
                if j.id == item_id:
                    del j

    def get_view(self) -> MenuView:
        from ...ref import bot
        from ...views import MenuView

        view = MenuView(bot=bot, menu_id=self.id, timeout=None)
        for index, item_set in enumerate(self.items):
            for item in item_set:
                view.add_item(item.get_item(self.id, index))  # type: ignore
        return view

    def get_description_embed(self, ctx: RiftContext) -> discord.Embed:
        from ...funcs import get_embed_author_guild

        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        desc = str(self.description).replace("\\n", "\n")
        return get_embed_author_guild(ctx.guild, desc, color=discord.Color.purple())

    async def new_interface(self, message: discord.Message) -> None:
        await MenuInterface.create(self, message)

    def __str__(self) -> str:
        if self.name is None:
            return f"{self.id}"
        return f"{self.id} - {self.name}"

    @property
    def items(self) -> List[List[MenuItem]]:
        return [
            [
                item
                for j in i
                if (item := cache.get_menu_item(j)) and item.guild_id == self.guild_id
            ]
            for i in self.item_ids
        ]


class MenuItem:
    __slots__ = ("id", "guild_id", "type", "data")

    def __init__(self, data: MenuItemData) -> None:
        self.id: int = data["id"]
        self.guild_id: int = data["guild"]
        self.type: str = data["type_"]
        self.data: Dict[str, Any] = data["data_"] or {}

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> MenuItem:
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        try:
            return await cls.fetch(convert_int(argument), ctx.guild.id)
        except ValueError:
            raise MenuItemNotFoundError(argument)

    @classmethod
    async def fetch(cls, item_id: int, guild_id: int) -> MenuItem:
        item = cache.get_menu_item(item_id)
        if item is None:
            raise MenuItemNotFoundError(item_id)
        if item.guild_id != guild_id:
            raise MenuItemNotFoundError(item_id)
        return item

    def get_item(self, menu_id: int, row: int) -> Union[MenuButton, MenuSelect]:
        from ...views import MenuButton, MenuSelect, MenuSelectOption

        custom_id = f"{menu_id}-{self.id}"
        if self.type == "button":
            return MenuButton(
                style=discord.ButtonStyle[self.data.get("style", "blurple")],
                label=l
                if (l := self.data.get("label", None)) or self.data.get("emoji", None)
                else "None",
                disabled=self.data.get("disabled", False),
                custom_id=custom_id,
                url=self.data.get("url", None),
                emoji=self.data.get("emoji", None),
                row=row,
                action=self.data.get("action", None),
                options=self.data.get("options", []),
            )
        elif self.type == "select":
            return MenuSelect(
                custom_id=custom_id,
                placeholder=self.data.get("placeholder", None),
                min_values=self.data.get("min_values", 1),
                max_values=self.data.get("max_values", 1),
                options=[
                    MenuSelectOption(
                        label=option["label"],
                        description=option.get("description", None),
                        emoji=option.get("emoji", None),
                        default=option.get("default", False),
                        action=self.data.get("action", None),
                        options=self.data.get("options", []),
                    )
                    for option in self.data["options"]
                ],
                row=row,
            )
        else:
            raise Exception(f"Unknown item type {self.type}")

    async def save(self) -> None:
        id = await execute_read_query(
            """
        INSERT INTO menu_items (guild, type_, data_) VALUES ($1, $2, $3) RETURNING id;
        """,
            self.guild_id,
            self.type,
            self.data,
        )
        self.id = id[0]["id"]
        cache.add_menu_item(self)

    @staticmethod
    def validate_flags(flags: Mapping[str, Any]) -> bool:
        if "action" in flags and flags.get("action", "ADD_ROLE")[0].upper().replace(
            " ", "_"
        ) not in {
            "ADD_ROLE",
            "REMOVE_ROLE",
            "ADD_ROLES",
            "REMOVE_ROLES",
            "TOGGLE_ROLE",
            "TOGGLE_ROLES",
            "CREATE_TICKET",
            "CLOSE_TICKET",
            "CREATE_TICKETS",
            "CLOSE_TICKETS",
            "CREATE_EMBASSY",
            "CLOSE_EMBASSY",
            "CREATE_EMBASSIES",
            "CLOSE_EMBASSIES",
        }:
            return False
        if "style" in flags and flags.get("style", ["red"])[0].lower() not in [
            "primary",
            "secondary",
            "success",
            "danger",
            "link",
            "blurple",
            "grey",
            "gray",
            "green",
            "red",
            "url",
        ]:
            return False
        return True

    @staticmethod
    async def format_flags(
        ctx: RiftContext, flags: Mapping[str, List[Any]]
    ) -> MenuFormattedFlags:  # sourcery no-metrics
        from ...funcs import get_embed_author_member
        from .embassy import Embassy, EmbassyConfig
        from .ticket import Ticket, TicketConfig

        formatted_flags: MenuFormattedFlags = {}
        if "action" in flags:
            formatted_flags["action"] = flags["action"][0].upper().replace(" ", "_")
        if "style" in flags:
            formatted_flags["style"] = flags["style"][0].lower()
        if "options" in flags and "action" in flags:
            formatted_flags["options"] = set()
            for i in flags["options"]:
                for j in i.split(" "):
                    if formatted_flags["action"] in {  # type: ignore
                        "ADD_ROLE",
                        "REMOVE_ROLE",
                        "ADD_ROLES",
                        "REMOVE_ROLES",
                        "TOGGLE_ROLE",
                        "TOGGLE_ROLES",
                    }:
                        try:
                            formatted_flags["options"].add(
                                (await commands.RoleConverter().convert(ctx, j)).id  # type: ignore
                            )
                        except commands.RoleNotFound as error:
                            if error.argument:
                                await ctx.reply(
                                    embed=get_embed_author_member(
                                        ctx.author,
                                        f"No role found with argument `{error.argument}`.\nPlease continue with further input, to correct please restart.",
                                    )
                                )
                    elif formatted_flags["action"] in {  # type: ignore
                        "CREATE_TICKET",
                        "CREATE_TICKETS",
                    }:
                        if j.isdigit():
                            try:
                                formatted_flags["options"].add(
                                    int(await TicketConfig.fetch(int(j)))
                                )
                            except TicketConfigNotFoundError:
                                await ctx.reply(
                                    embed=get_embed_author_member(
                                        ctx.author,
                                        f"No ticket found with ID `{j}`.\nPlease continue with further input, to correct please restart.",
                                    )
                                )
                    elif formatted_flags["action"] in {  # type: ignore
                        "CLOSE_TICKET",
                        "CLOSE_TICKETS",
                    }:
                        formatted_flags["options"].add(  # type: ignore
                            int(await Ticket.convert(ctx, j))
                        )
                    elif formatted_flags["action"] in {  # type: ignore
                        "CREATE_EMBASSY",
                        "CREATE_EMBASSIES",
                    }:
                        if j.isdigit():
                            try:
                                formatted_flags["options"].add(
                                    int(await EmbassyConfig.fetch(int(j)))
                                )
                            except EmbassyConfigNotFoundError:
                                await ctx.reply(
                                    embed=get_embed_author_member(
                                        ctx.author,
                                        f"No embassy found with ID `{j}`.\nPlease continue with further input, to correct please restart.",
                                    )
                                )
                    elif formatted_flags["action"] in {  # type: ignore
                        "CLOSE_EMBASSY",
                        "CLOSE_EMBASSIES",
                    }:
                        formatted_flags["options"].add(  # type: ignore
                            int(await Embassy.convert(ctx, j))
                        )
            formatted_flags["options"] = list(formatted_flags["options"])  # type: ignore
        for key, value in flags.items():
            if key not in formatted_flags:
                formatted_flags[key] = value[0]
        return formatted_flags

    def __str__(self) -> str:
        if self.type == "button":
            return f"ID: {self.id} - Type: {self.type} - Style: {self.data.get('style', 'blurple').capitalize()} - Label: {self.data.get('label', None)} - Disabled: {self.data.get('disabled', False)} - URL: {self.data.get('url', None)} - Emoji: {self.data.get('emoji', None)} - Row: {self.data.get('row', None)} - Action: {self.data.get('action', None)}"
        if self.type == "select":
            return f"ID: {self.id} - Type: {self.type} - Placeholder: {self.data.get('placeholder', None)} - Min Values: {self.data.get('min_values', 1)} - Max Values: {self.data.get('max_values', 1)}"
        return f"ID: {self.id} - Type: {self.type}"


class MenuInterface:
    __slots__ = ("menu_id", "message_id", "channel_id")

    def __init__(self, data: MenuInterfaceData) -> None:
        self.menu_id: int = data["menu"]
        self.message_id: int = data["message"]
        self.channel_id: int = data["channel"]

    @classmethod
    async def create(cls, menu: Menu, message: discord.Message) -> MenuInterface:
        interface = cls(
            {"menu": menu.id, "message": message.id, "channel": message.channel.id}
        )
        await interface.save()
        cache.add_menu_interface(interface)
        return interface

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO menu_interfaces (menu, message, channel) VALUES ($1, $2, $3);",
            self.menu_id,
            self.message_id,
            self.channel_id,
        )

    async def delete(self) -> None:
        await execute_query(
            "DELETE FROM menu_interfaces WHERE menu = $1 AND message = $2 AND channel = $3",
            self.menu_id,
            self.message_id,
            self.channel_id,
        )