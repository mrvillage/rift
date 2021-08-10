from asyncio import TimeoutError
from src.data.classes.menu import MenuItem
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ... import funcs
from ...checks import has_manage_permissions
from ...data.classes import Menu
from ...data.query import get_menus_user
from ...flags import ButtonFlags, SelectFlags, SelectOptionFlags
from ...ref import Rift


class Menus(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="menu",
        aliases=["menus", "role-menu", "rolemenu", "reaction-menu", "reactionmenu"],
        invoke_without_command=True,
    )
    @has_manage_permissions()
    async def menu(self, ctx: commands.Context, menu: Menu = None):
        # sourcery skip: merge-nested-ifs
        if ctx.invoked_with is not None:
            if ctx.invoked_with.lower() == "menus":
                await self.menu_list.invoke(ctx)
                return
        if menu is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You didn't specify a menu!"
                )
            )
        if TYPE_CHECKING:
            assert isinstance(menu, Menu)
        await ctx.send(str(menu))
        view = await menu.get_view()
        message = await ctx.reply("View", view=view)
        await menu.new_interface(message)

    @menu.command(name="list", aliases=["l", "li"])
    async def menu_list(self, ctx: commands.Context):
        menus = await get_menus_user(user_id=ctx.author.id)
        menus = [Menu(data=i) for i in menus]
        if menus:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "\n".join(str(i) for i in menus)
                )
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You don't have any menus!"
                )
            )

    @menu.command(name="create", aliases=["new"])
    @has_manage_permissions()
    async def menu_create(self, ctx: commands.Context):  # sourcery no-metrics
        message: discord.Message
        if TYPE_CHECKING:
            assert isinstance(ctx.message, discord.Message)
        menu = Menu.default(ctx.message.id, ctx.author.id)
        main_message = await ctx.reply(
            embed=funcs.get_embed_author_member(ctx.author, "Placeholder.")
        )
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
                if (
                    lower.startswith("finish")
                    or lower.startswith("cancel")
                    or lower.startswith("complete")
                    or lower.startswith("done")
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
                            if TYPE_CHECKING:
                                assert isinstance(flags["id"], str)
                            item = await MenuItem.fetch(int(flags["id"]))
                            if item.owner_id == ctx.author.id:
                                menu.add_item(item, row)
                                continue
                        except IndexError:
                            pass
                    if not MenuItem.validate_flags(flags):
                        await ctx.reply(
                            embed=funcs.get_embed_author_member(
                                ctx.author, "Invalid item."
                            )
                        )
                        continue
                    flags = await MenuItem.format_flags(ctx, flags)
                    item = MenuItem(
                        {
                            "item_id": message.id,
                            "owner_id": ctx.author.id,
                            "type_": "button",
                            "data_": flags,
                        }
                    )
                    menu.add_item(item, row)
                elif lower.startswith("select "):
                    flags = SelectFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "button", flags, menu.items
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
                        if (
                            lower.startswith("finish")
                            or lower.startswith("cancel")
                            or lower.startswith("complete")
                            or lower.startswith("done")
                        ):
                            break
                        if lower.startswith("option "):
                            flags = SelectOptionFlags.parse_flags(message.content[7:])
            else:
                if not any(menu.items):
                    return await ctx.reply(
                        embed=funcs.get_embed_author_member(
                            ctx.author, "You didn't add any items!"
                        )
                    )
                for row in menu.items:
                    for item in row:
                        await item.save()
                await menu.save()
                await main_message.reply(
                    embed=funcs.get_embed_author_member(ctx.author, "")
                )
        except TimeoutError:
            pass

    @menu.command(name="send", aliases=["post"])
    @has_manage_permissions()
    async def menu_send(
        self, ctx: commands.Context, menu: Menu, *, channel: discord.TextChannel
    ):
        view = await menu.get_view()
        embed = menu.get_description_embed(ctx)
        message = await channel.send(embed=embed, view=view)
        await menu.new_interface(message)


def setup(bot: Rift):
    bot.add_cog(Menus(bot))
