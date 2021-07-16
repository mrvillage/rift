from asyncio import TimeoutError
from src.data.query.menu import get_menu_item
from typing import Optional

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
    async def menus(self, ctx: commands.Context, menu: Optional[Menu]):
        if ctx.invoked_with.lower() == "menus":
            await self.menus_list.invoke(ctx)
            return
        await ctx.send(str(menu))
        menu = await Menu.fetch(1, ctx.author.id)
        view = await menu.get_view()
        message = await ctx.reply("View", view=view)
        await Menu.new_interface(message=ctx.message)

    @menus.command(name="list", aliases=["l", "li"])
    async def menus_list(self, ctx: commands.Context):
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

    @menus.command(name="create", aliases=["new"])
    async def menus_create(self, ctx: commands.Context):  # sourcery no-metrics
        message: discord.Message
        menu = Menu.default(ctx.message.id, ctx.author.id)
        main_message = await ctx.send(
            embed=funcs.get_embed_author_member(ctx.author, "Placeholder.")
        )
        try:
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
                if lower.startswith("button "):
                    flags = ButtonFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "button", flags, menu.items
                    )
                    if row == -1:
                        continue
                    if "id" in flags:
                        try:
                            item = await get_menu_item(item_id=flags["id"])
                            continue
                        except IndexError:
                            pass

                if lower.startswith("select "):
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
                            x = 1
        except TimeoutError:
            pass

    @menus.command(name="send", aliases=["post"])
    @has_manage_permissions()
    async def menus_send(
        self, ctx: commands.Context, menu: Menu, *, channel: discord.TextChannel
    ):
        view = await menu.get_view()
        embed = menu.get_description_embed(ctx)
        await channel.send(embed=embed, view=view)


def setup(bot: Rift):
    bot.add_cog(Menus(bot))
