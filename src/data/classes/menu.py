from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Union,
)

import discord
from discord.ext import commands

from ...cache import cache
from ...errors import MenuItemNotFoundError, MenuNotFoundError
from ..db import execute_query
from ..query import insert_interface
from .base import Makeable

__all__ = ("Menu", "MenuItem")

if TYPE_CHECKING:
    from typings import MenuData, MenuItemData


class View(discord.ui.View):
    def __init__(self, *args, **kwargs) -> None:
        self.menu_id = kwargs.pop("menu_id")
        self.bot = kwargs.pop("bot")
        super().__init__(*args, **kwargs)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert isinstance(interaction.message, discord.Message)
        return bool(
            [
                i
                for i in cache.menu_interfaces
                if i["menu_id"] == self.menu_id
                and i["message_id"] == interaction.message.id
            ]
        )


class Button(discord.ui.Button):
    def __init__(self, *args, **kwargs) -> None:
        self.action = kwargs.pop("action")
        self.options = kwargs.pop("options")
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction) -> None:
        # sourcery no-metrics
        from ...funcs import get_embed_author_member
        from ..get import get_link_user
        from .alliance import Alliance
        from .embassy import EmbassyConfig
        from .nation import Nation
        from .ticket import TicketConfig

        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
            assert isinstance(interaction.guild, discord.Guild)
        bot_member = interaction.guild.get_member(interaction.application_id)
        if TYPE_CHECKING:
            assert isinstance(bot_member, discord.Member)
        highest_role = bot_member.top_role
        if self.action is None:
            return await interaction.response.defer()
        if self.action in {"ADD_ROLE", "ADD_ROLES"}:
            roles = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    roles.append(role)
            if roles:
                await interaction.user.add_roles(*roles)
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Added the following roles: {', '.join(role.mention for role in roles)}",
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were added since you have them all already.",
                    ),
                )
        elif self.action in {"REMOVE_ROLE", "REMOVE_ROLES"}:
            roles = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    roles.append(role)
            if roles:
                await interaction.user.remove_roles(*roles)
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Removed the following roles from you: {', '.join(role.mention for role in roles)}",
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were removed since you you don't have any of them.",
                    ),
                )
        elif self.action in {"CREATE_TICKET", "CREATE_TICKETS"}:
            await interaction.response.defer()
            configs = [await TicketConfig.fetch(opt) for opt in self.options]
            tickets = []
            for config in configs:
                if config.guild_id != interaction.guild.id:
                    continue
                ticket = await config.create(interaction.user)
                await ticket.start(interaction.user, config)
                tickets.append(ticket)
            if len(tickets) > 1:
                tickets = "\n".join(f"<#{ticket.id}" for ticket in tickets)
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user, f"Tickets Created!\n{tickets}"
                    ),
                )
            else:
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user, f"Ticket Created!\n<#{tickets[0].id}>"
                    ),
                )
        elif self.action in {"CLOSE_TICKET", "CREATE_TICKETS"}:
            ...
        elif self.action in {"CREATE_EMBASSY", "CREATE_EMBASSIES"}:
            await interaction.response.defer()
            configs = [await EmbassyConfig.fetch(opt) for opt in self.options]
            embassies = []
            try:
                nation = await get_link_user(interaction.user.id)
                nation = await Nation.fetch(nation["nation_id"])
                alliance = await Alliance.fetch(nation.alliance_id)
                if nation.alliance_position not in {"Officer", "Heir", "Leader"}:
                    raise KeyError
            except IndexError:
                return await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "You must be linked to create an embassy.",
                        color=discord.Color.red(),
                    ),
                )
            except KeyError:
                return await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "You must be an Officer or higher to create an embassy.",
                        color=discord.Color.red(),
                    ),
                )
            for config in configs:
                if config.guild_id != interaction.guild.id:
                    continue
                embassy, start = await config.create(interaction.user, alliance)
                if start:
                    await embassy.start(interaction.user, config)
                embassies.append(embassy)
            if len(embassies) > 1:
                embassies = "\n".join(
                    f"<#{embassy.id}" for embassy in embassies
                )
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user, f"Embassies:\n{embassies}"
                    ),
                )
            else:
                await interaction.followup.send(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user, f"Embassy:\n<#{embassies[0].id}>"
                    ),
                )
        elif self.action in {"CLOSE_EMBASSY", "CLOSE_EMBASSIES"}:
            ...


class Select(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction) -> None:
        values = self.values.copy()


class SelectOption(discord.SelectOption):
    def __init__(self, *args, **kwargs) -> None:
        self.action = kwargs.pop("action")
        self.options = kwargs.pop("options")
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"Label: {self.label} - Description: {self.description} - Emoji: {self.emoji} - Default: {self.default} - Action: {self.action}"


class Menu(Makeable):
    id: int
    items: Sequence[List[MenuItem]]
    name: Optional[str]
    description: Optional[str]
    item_ids: Sequence[Sequence[int]]
    permissions: Mapping[str, Any]

    __slots__ = (
        "id",
        "guild_id",
        "name",
        "description",
        "item_ids",
        "permissions",
        "items",
    )

    def __init__(self, data: MenuData) -> None:
        self.id = data["id"]
        self.guild_id = data["guild_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.item_ids = data["items"] or []
        self.permissions = data["permissions"] or {}

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Menu:
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        try:
            return await cls.fetch(int(argument), ctx.guild.id)
        except ValueError:
            raise MenuNotFoundError(argument)

    @classmethod
    async def fetch(cls, menu_id: int, guild_id: int) -> Menu:
        menu = cache.get_menu(menu_id, guild_id)
        if menu:
            return menu
        raise MenuNotFoundError(menu_id)

    @classmethod
    def default(cls, menu_id: int, guild_id: int) -> Menu:
        menu = cls(
            data={  # type: ignore
                "id": menu_id,
                "guild_id": guild_id,
                "name": None,
                "description": None,
                "items": [],
                "permissions": {},
            }
        )
        menu.items = [[], [], [], [], []]
        return menu

    async def _make_items(self) -> None:
        items = []
        for i in self.item_ids:
            if i:
                items.append([(await MenuItem.fetch(j, self.guild_id)) for j in i])
            else:
                items.append([])
        self.items = items

    async def set_(self, **kwargs: Mapping[str, Any]) -> Menu:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        await execute_query(
            f"""
        UPDATE menus SET {sets} WHERE id = $1;
        """,
            self.id,
            *args,
        )
        return self

    async def save(self) -> None:
        await execute_query(
            """
        INSERT INTO menus (id, guild_id, name, description, items, permissions) VALUES ($1, $2, $3, $4, $5, $6);
        """,
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
            self.permissions or None,
        )

    def add_item(self, item: MenuItem, row: int) -> None:
        self.items[row].append(item)

    def remove_item(self, item_id: str) -> None:
        for i in self.items:
            for j in i:
                if j.id == item_id:
                    del j

    async def get_view(self) -> View:
        from ...ref import bot

        await self.make_attrs("items")
        self.view = View(bot=bot, menu_id=self.id, timeout=None)
        for index, item_set in enumerate(self.items):
            for item in item_set:
                self.view.add_item(item.get_item(self.id, index))
        return self.view

    def get_description_embed(self, ctx: commands.Context) -> discord.Embed:
        from ...funcs import get_embed_author_guild

        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        desc = str(self.description).replace("\\n", "\n")
        self.embed = get_embed_author_guild(ctx.guild, desc)
        return self.embed

    async def new_interface(self, message: discord.Message) -> None:
        await insert_interface(menu_id=self.id, message=message)

    def __str__(self) -> str:
        if self.name is None:
            return f"{self.id}"
        return f"{self.id} - {self.name}"


class MenuItem:
    __slots__ = ("id", "guild_id", "type", "data")

    def __init__(self, data: MenuItemData) -> None:
        self.id = data["id"]
        self.guild_id = data["guild_id"]
        self.type = data["type_"]
        self.data = data["data_"] or {}

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> MenuItem:
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        try:
            return await cls.fetch(int(argument), ctx.guild.id)
        except ValueError:
            raise MenuItemNotFoundError(argument)

    @classmethod
    async def fetch(cls, item_id: int, guild_id: int) -> MenuItem:
        item = cache.get_menu_item(item_id, guild_id)
        if item:
            return item
        raise MenuItemNotFoundError(item_id)

    def get_item(self, menu_id: int, row: int) -> Union[Button, Select]:
        custom_id = f"{menu_id}-{self.id}"
        if self.type == "button":
            return Button(
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
            return Select(
                custom_id=custom_id,
                placeholder=self.data.get("placeholder", None),
                min_values=self.data.get("min_values", 1),
                max_values=self.data.get("max_values", 1),
                options=[
                    SelectOption(
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
        await execute_query(
            """
        INSERT INTO menu_items (id, guild_id, type_, data_) VALUES ($1, $2, $3, $4);
        """,
            self.id,
            self.guild_id,
            self.type,
            self.data,
        )

    @staticmethod
    def validate_flags(flags: Mapping[str, Any]) -> bool:
        if "action" in flags and flags.get("action", "ADD_ROLE")[0].upper().replace(
            " ", "_"
        ) not in {
            "ADD_ROLE",
            "REMOVE_ROLE",
            "ADD_ROLES",
            "REMOVE_ROLES",
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
        ctx: commands.Context, flags: Mapping[str, List[Any]]
    ) -> MutableMapping[str, Any]:  # sourcery no-metrics
        from ...funcs import get_embed_author_member
        from .embassy import Embassy, EmbassyConfig
        from .ticket import Ticket, TicketConfig

        formatted_flags = {}
        if "action" in flags:
            formatted_flags["action"] = flags["action"][0].upper().replace(" ", "_")
        if "style" in flags:
            formatted_flags["style"] = flags["style"][0].lower()
        if "options" in flags:
            formatted_flags["options"] = set()
            for i in flags["options"]:
                for j in i.split(" "):
                    if formatted_flags["action"] in {
                        "ADD_ROLE",
                        "REMOVE_ROLE",
                        "ADD_ROLES",
                        "REMOVE_ROLES",
                    }:
                        try:
                            formatted_flags["options"].add(
                                (await commands.RoleConverter().convert(ctx, j)).id
                            )
                        except commands.RoleNotFound as error:
                            if error.argument:
                                await ctx.reply(
                                    embed=get_embed_author_member(
                                        ctx.author,
                                        f"No role found with argument `{error.argument}`.\nPlease continue with further input, to correct please restart.",
                                    )
                                )
                    elif formatted_flags["action"] in {
                        "CREATE_TICKET",
                        "CREATE_TICKETS",
                    }:
                        if j.isdigit():
                            try:
                                formatted_flags["options"].add(
                                    int(await TicketConfig.fetch(int(j)))
                                )
                            except IndexError:
                                await ctx.reply(
                                    embed=get_embed_author_member(
                                        ctx.author,
                                        f"No ticket found with ID `{j}`.\nPlease continue with further input, to correct please restart.",
                                    )
                                )
                    elif formatted_flags["action"] in {"CLOSE_TICKET", "CLOSE_TICKETS"}:
                        formatted_flags["options"].add(
                            int(await Ticket.convert(ctx, j))
                        )
                    elif formatted_flags["action"] in {
                        "CREATE_EMBASSY",
                        "CREATE_EMBASSIES",
                    }:
                        if j.isdigit():
                            try:
                                formatted_flags["options"].add(
                                    int(await EmbassyConfig.fetch(int(j)))
                                )
                            except IndexError:
                                await ctx.reply(
                                    embed=get_embed_author_member(
                                        ctx.author,
                                        f"No embassy found with ID `{j}`.\nPlease continue with further input, to correct please restart.",
                                    )
                                )
                    elif formatted_flags["action"] in {
                        "CLOSE_EMBASSY",
                        "CLOSE_EMBASSIES",
                    }:
                        formatted_flags["options"].add(
                            int(await Embassy.convert(ctx, j))
                        )
            formatted_flags["options"] = list(formatted_flags["options"])
        for key, value in flags.items():
            if key not in formatted_flags:
                formatted_flags[key] = value[0]
        return formatted_flags

    def __str__(self) -> str:
        if self.type == "button":
            return f"ID: {self.id} - Type: {self.type} - Style: {self.data.get('style', 'blurple').capitalize()} - Label: {self.data.get('label', None)} - Disabled: {self.data.get('disabled', False)} - URL: {self.data.get('url', None)} - Emoji: {self.data.get('emoji', None)} - Row: {self.data.get('row', None)} - Action: {self.data.get('action', None)}"
        if self.type == "select":
            return f"ID: {self.id} - Type: {self.type} - Placeholder: {self.data.get('placeholder', None)} - Min Values: {self.data.get('min_values', 1)} - Max Values: {self.data.get('max_values', 1)} - Options: {', '.join(str(option) for option in self.data.get('options', [None]))}"
        return f"ID: {self.id} - Type: {self.type}"
