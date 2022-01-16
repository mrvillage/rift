from __future__ import annotations

import datetime
from typing import Literal, Union

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...data.classes import Alliance, Grant, Resources
from ...enums import GrantPayoff, GrantStatus
from ...errors import EmbedErrorMessage, NoRolesError
from ...ref import Rift, RiftContext


class Grants(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="grant",
        brief="A group of commands related to grants.",
        type=commands.CommandType.chat_input,
    )
    async def grant(self, ctx: RiftContext):
        ...

    @grant.command(  # type: ignore
        name="send", brief="Send a grant.", type=commands.CommandType.chat_input
    )
    async def grant_send(
        self,
        ctx: RiftContext,
        recipient: Union[discord.Member, discord.User],
        resources: Resources,
        payoff: Literal["NONE", "DEPOSIT"],
        note: str = MISSING,
        deadline: str = MISSING,
        alliance: Alliance = MISSING,
        request: bool = True,
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        time = datetime.datetime.utcnow()
        if deadline is not MISSING:
            try:
                deadline_datetime = datetime.datetime.fromtimestamp(
                    time.timestamp() + funcs.utils.parse_time_to_seconds(deadline)
                )
            except ValueError:
                raise EmbedErrorMessage(ctx.author, "Invalid time format.")
        else:
            deadline_datetime = None
        permissions = alliance.permissions_for(ctx.author)
        if not (permissions.leadership or permissions.manage_grants):
            raise NoRolesError(alliance, "Manage Grants")
        payoff_ = getattr(GrantPayoff, payoff)
        if payoff_ is not GrantPayoff.NONE:
            request = True
        grant = await Grant.create(
            recipient,
            time,
            resources,
            alliance,
            payoff_,
            note or None,
            deadline_datetime,
            Resources(),
            GrantStatus.PENDING,
        )
        await grant.send(ctx.author, request)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Sent a grant with ID {grant.id} from alliance {alliance} to <@{recipient.id}> for {resources} with a payoff method of `{payoff}` and {'no deadline' if deadline_datetime is None else f'a deadline at <t:{deadline_datetime.timestamp()}:R>'} and a note of {note}.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )


def setup(bot: Rift):
    bot.add_cog(Grants(bot))
