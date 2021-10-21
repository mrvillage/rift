from __future__ import annotations

from asyncio import TimeoutError
from typing import TYPE_CHECKING, List, Optional

import discord
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...checks import has_manage_permissions
from ...data.classes import Menu, MenuItem
from ...errors import MenuItemNotFoundError
from ...flags import ButtonFlags, SelectFlags, SelectOptionFlags
from ...ref import Rift, RiftContext


class Menus(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="menu",
        aliases=["menus", "role-menu", "rolemenu", "reaction-menu", "reactionmenu"],
        brief="A group of commands related to menus.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu(self, ctx: RiftContext, menu: Optional[Menu] = None):
        ...

    @menu.command(  # type: ignore
        name="list",
        aliases=["l", "li"],
        brief="List the menu configurations for this guild.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_list(self, ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        menus = [i for i in cache.menus if i.guild_id == ctx.guild.id]
        if menus:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "\n".join(str(i) for i in menus),
                    color=discord.Color.blue(),
                )
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No menus found for this server!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

    @menu.command(  # type: ignore
        name="create",
        aliases=["new"],
        brief="Create a new menu configuration.",
        type=commands.CommandType.chat_input,
        descriptions={"description": "The description to send with the menu."},
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_create(
        self, ctx: RiftContext, *, description: Optional[str] = None
    ):  # sourcery no-metrics
        message: discord.Message
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        menu = Menu.default(ctx.guild.id)
        menu.description = (
            description
            or "This is a menu! Someone was lazy and didn't put a description. :)"
        )
        # will have to update for buttons and selects
        # when selects are added and work properly
        main_message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "Waiting for followup messages to assemble a menu...\n\nEach message should look something like this: `button <flags>` where flags is something like `label: This is a label style: gray action: CREATE_TICKET options: 1234`. The following are valid flags:\naction: The action to perform when the button is clicked, can be nothing or any of CREATE_TICKET, CREATE_TICKETS, ADD_ROLE, ADD_ROLES, CREATE_EMBASSY, or CREATE_EMBASSIES.\nurl: The url to navigate to when the button is clicked, if specified the only other valid options are row, label, and emoji.\ndisabled: Whether the button should be disabled or not, accepts a boolean like yes or no.\nstyle: The style of the button, can be any of primary, secondary, success, danger, link, blurple, grey, gray, green, red, or url.\nlabel: The label for the button, must be present if emoji is not.\nemoji: The emoji to put on the button, must be present if label is not.\noptions: A space separated list of options for the action, can be embassy or ticket configs or roles.\nrow: The row to put the button on, can be and number from 1 through 5.\nid: The ID of the menu item, can be used instead of the above options to use a specific item that's already created.",
                color=discord.Color.blue(),
            ),
            return_message=True,
        )
        items: List[List[MenuItem]] = [[], [], [], [], []]
        try:
            running = True
            while running:
                message = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author.id == ctx.author.id
                    and message.channel.id == ctx.channel.id,
                    timeout=300,
                )
                lower = message.content.lower()
                if lower.startswith(
                    ("finish", "cancel", "complete", "done", "save", "stop")
                ):
                    running = False
                    continue
                if lower.startswith("button "):
                    flags = ButtonFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "button", flags, menu.items
                    )
                    if row is None:
                        continue
                    if "id" in flags:
                        try:
                            item = await MenuItem.fetch(
                                int(flags["id"][0]), ctx.guild.id
                            )
                            items[row].append(item)
                            continue
                        except MenuItemNotFoundError:
                            pass
                    if not MenuItem.validate_flags(flags):
                        await ctx.reply(
                            embed=funcs.get_embed_author_member(
                                ctx.author, "Invalid item.", color=discord.Color.red()
                            )
                        )
                        continue
                    flags = await MenuItem.format_flags(ctx, flags)
                    item = MenuItem(
                        {  # type: ignore
                            "guild_id": ctx.guild.id,
                            "type_": "button",
                            "data_": flags,
                        }
                    )
                    items[row].append(item)
                elif lower.startswith("select "):
                    flags = SelectFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "select", flags, menu.items
                    )
                    if row == -1:
                        continue
                    while True:
                        message = await self.bot.wait_for(
                            "message",
                            check=lambda message: message.author.id == ctx.author.id
                            and message.channel.id == ctx.channel.id,
                            timeout=300,
                        )
                        lower = message.content.lower()
                        if lower.startswith(
                            ("finish", "cancel", "complete", "done", "save", "stop")
                        ):
                            break
                        if lower.startswith("option "):
                            flags = SelectOptionFlags.parse_flags(message.content[7:])
            else:
                if not any(items):
                    return await ctx.reply(
                        embed=funcs.get_embed_author_member(
                            ctx.author,
                            "You didn't add any items!",
                            color=discord.Color.red(),
                        )
                    )
                for index, row in enumerate(items):
                    for item in row:
                        await item.save()
                        menu.add_item(item, index)
                await menu.save()
                await main_message.reply(  # type: ignore
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"Menu ID: {menu.id}\n\n"
                        + "\n\n".join(str(j) for i in menu.items for j in i),
                        color=discord.Color.green(),
                    )
                )
        except TimeoutError:
            await main_message.reply(  # type: ignore
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Menu creation timed out. Please try again.",
                    color=discord.Color.red(),
                )
            )

    @menu.command(  # type: ignore
        name="send",
        aliases=["post"],
        brief="Send a menu configuration to a channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "menu": "The menu to send.",
            "channel": "The channel to send the menu to.",
        },
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_send(
        self, ctx: RiftContext, menu: Menu, *, channel: discord.TextChannel
    ):
        view = menu.get_view()
        embed = menu.get_description_embed(ctx)
        message = await channel.send(embed=embed, view=view)
        await menu.new_interface(message)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Menu {menu.id} sent to {channel.mention}!",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @menu.command(  # type: ignore
        name="info",
        aliases=["details"],
        brief="Get information about a menu configuration.",
        type=commands.CommandType.chat_input,
        descriptions={
            "menu": "The menu to get information about.",
        },
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_info(self, ctx: RiftContext, *, menu: Menu):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Menu ID: {menu.id}\nDescription:\n\n{menu.description}\n",
                fields=[
                    {"name": "\u200b", "value": str(j)} for i in menu.items for j in i
                ],
                color=discord.Color.green(),
            )
        )

    @menu.command(  # type: ignore
        name="item",
        aliases=["items"],
        brief="Get information about a menu item.",
        type=commands.CommandType.chat_input,
        descriptions={
            "item": "The menu item to get information about.",
        },
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_item(self, ctx: RiftContext, *, item: MenuItem):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                str(item) + f"\nOptions: {None if (o := item.data.get('options', None)) is not None else ', '.join(r.mention for i in o if(r := ctx.guild.get_role(i))) if item.data.get('action') in {'ADD_ROLE', 'REMOVE_ROLE', 'ADD_ROLES', 'REMOVE_ROLES'} else ', '.join(str(i) for i in o)}",  # type: ignore
                color=discord.Color.green(),
            )
        )

    @menu.command(  # type: ignore
        name="edit",
        brief="Create a new menu configuration.",
        type=commands.CommandType.chat_input,
        descriptions={"description": "The new description to send with the menu."},
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_edit(
        self, ctx: RiftContext, menu: Menu, description: Optional[str] = None
    ):  # sourcery no-metrics
        message: discord.Message
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        new_menu = Menu.default(ctx.guild.id)
        new_menu.description = description or menu.description
        # will have to update for buttons and selects
        # when selects are added and work properly
        main_message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "Waiting for followup messages to reassemble a menu...\n\nEach message should look something like this: `button <flags>` where flags is something like `label: This is a label style: gray action: CREATE_TICKET options: 1234`. The following are valid flags:\naction: The action to perform when the button is clicked, can be nothing or any of CREATE_TICKET, CREATE_TICKETS, ADD_ROLE, ADD_ROLES, CREATE_EMBASSY, or CREATE_EMBASSIES.\nurl: The url to navigate to when the button is clicked, if specified the only other valid options are row, label, and emoji.\ndisabled: Whether the button should be disabled or not, accepts a boolean like yes or no.\nstyle: The style of the button, can be any of primary, secondary, success, danger, link, blurple, grey, gray, green, red, or url.\nlabel: The label for the button, must be present if emoji is not.\nemoji: The emoji to put on the button, must be present if label is not.\noptions: A space separated list of options for the action, can be embassy or ticket configs or roles.\nrow: The row to put the button on, can be and number from 1 through 5.\nid: The ID of the menu item, can be used instead of the above options to use a specific item that's already created.",
                color=discord.Color.blue(),
            ),
            return_message=True,
        )
        items: List[List[MenuItem]] = [[], [], [], [], []]
        try:
            running = True
            while running:
                message = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author.id == ctx.author.id
                    and message.channel.id == ctx.channel.id,
                    timeout=300,
                )
                lower = message.content.lower()
                if lower.startswith(
                    ("finish", "cancel", "complete", "done", "save", "stop")
                ):
                    running = False
                    continue
                if lower.startswith("button "):
                    flags = ButtonFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "button", flags, new_menu.items
                    )
                    if row is None:
                        continue
                    if "id" in flags:
                        try:
                            item = await MenuItem.fetch(
                                int(flags["id"][0]), ctx.guild.id
                            )
                            items[row].append(item)
                            continue
                        except MenuItemNotFoundError:
                            pass
                    if not MenuItem.validate_flags(flags):
                        await ctx.reply(
                            embed=funcs.get_embed_author_member(
                                ctx.author, "Invalid item.", color=discord.Color.red()
                            )
                        )
                        continue
                    flags = await MenuItem.format_flags(ctx, flags)
                    item = MenuItem(
                        {  # type: ignore
                            "guild_id": ctx.guild.id,
                            "type_": "button",
                            "data_": flags,
                        }
                    )
                    items[row].append(item)
                elif lower.startswith("select "):
                    flags = SelectFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "select", flags, new_menu.items
                    )
                    if row == -1:
                        continue
                    while True:
                        message = await self.bot.wait_for(
                            "message",
                            check=lambda message: message.author.id == ctx.author.id
                            and message.channel.id == ctx.channel.id,
                            timeout=300,
                        )
                        lower = message.content.lower()
                        if lower.startswith(
                            ("finish", "cancel", "complete", "done", "save", "stop")
                        ):
                            break
                        if lower.startswith("option "):
                            flags = SelectOptionFlags.parse_flags(message.content[7:])
            else:
                if not any(items):
                    return await ctx.reply(
                        embed=funcs.get_embed_author_member(
                            ctx.author,
                            "You didn't add any items!",
                            color=discord.Color.red(),
                        )
                    )
                menu.item_ids = new_menu.item_ids
                menu.description = new_menu.description
                menu.name = new_menu.name
                for index, row in enumerate(items):
                    for item in row:
                        if item.id is None:
                            await item.save()
                        menu.add_item(item, index)
                await menu.save()
                interfaces = [
                    i for i in cache.menu_interfaces if i["menu_id"] == menu.id
                ]
                view = menu.get_view()
                embed = menu.get_description_embed(ctx)
                for interface in interfaces:
                    channel = self.bot.get_channel(interface["channel_id"])
                    if channel is None:
                        continue
                    if TYPE_CHECKING:
                        assert isinstance(channel, discord.TextChannel)
                    partial_message = channel.get_partial_message(
                        interface["message_id"]
                    )
                    await partial_message.edit(embed=embed, view=view)
                await main_message.reply(  # type: ignore
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"Menu {menu.id} has been edited and all interfaces updated!\n\n"
                        + "\n\n".join(str(j) for i in menu.items for j in i),
                        color=discord.Color.green(),
                    )
                )
        except TimeoutError:
            await main_message.reply(  # type: ignore
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Menu edit timed out. Please try again.",
                    color=discord.Color.red(),
                )
            )


def setup(bot: Rift):
    bot.add_cog(Menus(bot))
