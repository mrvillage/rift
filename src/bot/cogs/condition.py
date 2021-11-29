from __future__ import annotations

import discord
from discord.ext import commands
from discord.utils import MISSING

from src.errors.invalid import InvalidConditionError

from ... import funcs
from ...cache import cache
from ...data.classes import Condition
from ...ref import Rift, RiftContext
from ...views import Confirm


class Conditions(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="condition",
        brief="Manage conditions.",
        type=commands.CommandType.chat_input,
    )
    async def condition(self, ctx: RiftContext):
        ...

    @condition.command(  # type: ignore
        name="add", brief="Add a condition.", type=commands.CommandType.chat_input
    )
    async def condition_add(
        self, ctx: RiftContext, condition: Condition, name: str = MISSING
    ):
        condition.name = name
        view = Confirm(timeout=3)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Are you sure you want to add a condition?\n\n`{condition}`",
                color=discord.Color.orange(),
            ),
            view=view,
            ephemeral=True,
        )
        if await view.wait():
            await ctx.edit(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Condition confirmation timed out, please try again.",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        elif view.value:
            await condition.save()
            await view.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Added condition #{condition.id:,}{'with name '+name if name else ''} and condition `{condition}`.",
                    color=discord.Color.green(),
                ),
                view=None,
            )
        else:
            await view.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author, "Condition cancelled.", color=discord.Color.red()
                ),
                view=None,
            )

    @condition.command(  # type: ignore
        name="remove", brief="Remove a condition.", type=commands.CommandType.chat_input
    )
    async def condition_remove(self, ctx: RiftContext, condition: Condition):
        if condition.id is None:
            raise InvalidConditionError(condition)
        await condition.remove()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Removed condition #{condition.id:,}.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @condition.command(  # type: ignore
        name="list",
        brief="List all your conditions.",
        type=commands.CommandType.chat_input,
    )
    async def condition_list(self, ctx: RiftContext):
        conditions = [i for i in cache.conditions if i.owner_id == ctx.author.id]
        if not conditions:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have any conditions!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You have {len(conditions)} condition{'s' if len(conditions) > 1 else ''}:\n\n"
                + "\n".join(
                    f"#{i.id:,} {' - ' + i.name if i.name else ''}" for i in conditions
                ),
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @condition.command(  # type: ignore
        name="info",
        brief="Get information about a condition.",
        type=commands.CommandType.chat_input,
    )
    async def condition_info(self, ctx: RiftContext, condition: Condition):
        if condition.id is None:
            raise InvalidConditionError(condition)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Condition #{condition.id:,}:\n\n`{condition}`",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )


def setup(bot: Rift):
    bot.add_cog(Conditions(bot))
