from __future__ import annotations

from typing import Optional

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...data.classes import Condition
from ...errors import EmbedErrorMessage, InvalidConditionError
from ...ref import Rift, RiftContext


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
        name="add",
        brief="Add a condition.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to add.",
            "name": "The name of the condition.",
            "public": "Whether the condition is public or not.",
        },
    )
    async def condition_add(
        self,
        ctx: RiftContext,
        condition: Condition,
        name: Optional[str] = None,
        public: bool = False,
    ):
        condition.name = name
        condition.public = public
        await condition.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Added {'public ' if public else ''} condition #{condition.id} {'with name '+name if name else ''} and condition `{condition}`.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @condition.command(  # type: ignore
        name="remove",
        brief="Remove a condition.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to remove.",
        },
    )
    async def condition_remove(self, ctx: RiftContext, condition: Condition):
        if condition.owner_id != ctx.author.id:
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
    async def condition_list(self, ctx: RiftContext, public: bool = False):
        conditions = [i for i in cache.conditions if i.owner_id == ctx.author.id]
        if not conditions:
            raise EmbedErrorMessage(
                ctx.author,
                "You don't have any conditions!",
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
        if condition.id == 0:
            raise InvalidConditionError(condition)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{'Public condition' if condition.public else 'Condition'} #{condition.id}:\n\n`{condition}`",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @condition.command(  # type: ignore
        name="edit",
        brief="Edit a condition.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to edit.",
            "value": "The new value of the condition.",
            "name": "The name of the condition.",
            "public": "Whether the condition is public or not.",
        },
    )
    async def condition_edit(
        self,
        ctx: RiftContext,
        condition: Condition,
        value: Condition = MISSING,
        name: Optional[str] = MISSING,
        public: bool = MISSING,
    ):
        if condition.owner_id != ctx.author.id:
            raise InvalidConditionError(condition)
        if value is not MISSING and value.id != 0:
            raise InvalidConditionError(value)
        if value is not MISSING:
            condition.condition = value.condition
        if name is not MISSING:
            condition.name = name
        if public is not MISSING:
            condition.public = public
        await condition.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Edited condition #{condition.id} to {'' if condition.public else 'not '}be public with {f'name {condition.name}' if condition.name is not None else 'no name'} and condition `{condition}`.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )


def setup(bot: Rift):
    bot.add_cog(Conditions(bot))
