from __future__ import annotations

from typing import Optional

import discord
from discord.ext import commands
from discord.utils import MISSING

from src.errors.credentials import NoCredentialsError

from ... import funcs
from ...cache import cache
from ...data.classes import Alliance, Resources
from ...errors import NoRolesError
from ...ref import Rift, RiftContext
from ...views import Confirm


class Bank(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="bank",
        brief="A group of commands related to your alliance bank.",
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    async def bank(self, ctx: RiftContext):
        ...

    @bank.command(  # type: ignore
        name="transfer",
        brief="Send money from an alliance bank.",
        type=commands.CommandType.chat_input,
        descriptions={
            "recipient": "The nation or alliance to send to.",
            "resources": "The resources to send.",
            "alliance": "The alliance to send money from, defaults to your alliance.",
        },
    )
    async def bank_transfer(
        self,
        ctx: RiftContext,
        recipient: str,
        resources: Resources,
        alliance: Alliance = MISSING,
        note: Optional[str] = None,
    ):
        recipient_ = await funcs.convert_nation_or_alliance(ctx, recipient)
        alliance_ = alliance or await Alliance.convert(ctx, None)
        if alliance_ is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance and didn't specify one to send from! Please try again with an alliance.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        alliance = alliance_
        if not len(resources):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't give any valid resources!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        roles = [
            i
            for i in cache.roles
            if i.alliance_id == alliance.id
            and ctx.author.id in i.member_ids
            and (i.permissions.send_alliance_bank or i.permissions.leadership)
        ]
        if not roles:
            raise NoRolesError(alliance, "Send Alliance Bank")
        view = Confirm(defer=True)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Are you sure you want to transfer {resources} to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}** from the alliance of **{repr(alliance)}**",
                color=discord.Color.orange(),
            ),
            view=view,
            ephemeral=True,
        )
        r = await view.wait()
        if r:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't confirm the transaction in time!",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        if not view.value:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"You have cancelled the transfer of {resources} from **{repr(alliance)}** to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}**.",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Sending {resources} from **{repr(alliance)}** to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}**...",
                color=discord.Color.orange(),
            ),
            view=None,
        )
        credentials = funcs.credentials.find_highest_alliance_credentials(
            alliance, "send_alliance_bank"
        )
        if credentials is None or (
            credentials.username is None and credentials.password is None
        ):
            raise NoCredentialsError()
        complete = await funcs.withdraw(
            resources,
            recipient_,
            credentials,
            note=f"Transfer by {ctx.author.name}#{ctx.author.discriminator} with note: {note}",
        )
        if not complete:
            return await ctx.interaction.edit_original_message(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Something went wrong with the transaction. Please try again.",
                    color=discord.Color.red(),
                )
            )
        await ctx.interaction.edit_original_message(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"You successfully transferred {resources} from **{repr(alliance)}** to the **{type(recipient_).__name__.lower()}** of **{repr(recipient_)}**.",
                color=discord.Color.green(),
            )
        )

    @bank.command(  # type: ignore
        name="balance",
        aliases=["bal"],
        brief="Check the balance of an alliance bank.",
        type=commands.CommandType.chat_input,
        descriptions={
            "alliance": "The alliance to check the balance of, defaults to your alliance.",
        },
    )
    async def bank_balance(self, ctx: RiftContext, *, alliance: Alliance = MISSING):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        roles = [
            i
            for i in cache.roles
            if i.alliance_id == alliance.id
            and ctx.author.id in i.member_ids
            and (i.permissions.view_alliance_bank or i.permissions.leadership)
        ]
        if not roles:
            raise NoRolesError(alliance, "View Alliance Bank")
        resources = await alliance.fetch_bank()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The **{repr(alliance)}** alliance bank has {resources}.",
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Bank(bot))
