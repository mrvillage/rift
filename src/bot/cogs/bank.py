from asyncio import TimeoutError
from typing import TYPE_CHECKING, Union

import discord
from discord.ext import commands

from ... import find, funcs, perms
from ...data.classes import Alliance, Nation
from ...data.classes.bank import Transaction
from ...errors import AllianceNotFoundError, NationNotFoundError, RecipientNotFoundError
from ...ref import Rift
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
    async def bank(self, ctx: commands.Context):
        ...

    @commands.command(
        name="send", brief="Send money from your alliance bank.", hidden=True
    )
    async def send(self, ctx: commands.Context, recipient, *, resources: Transaction):
        await ctx.invoke(self.bank_transfer, recipient, resources=resources)

    @bank.command(
        name="transfer",
        aliases=["send"],
        brief="Send money from your alliance bank.",
        type=commands.CommandType.chat_input,
        descriptions={
            "recipient": "The nation or alliance to send to.",
            "transaction": "The resources to send.",
        },
    )
    async def bank_transfer(
        self,
        ctx: commands.Context,
        recipient: Union[Alliance, Nation],
        *,
        resources: Transaction,
    ):  # sourcery no-metrics
        if isinstance(recipient, Alliance):
            author = ctx.guild
        else:
            await recipient.make_attrs("user")
            author = recipient.user
        if TYPE_CHECKING:
            assert author is not None
        try:
            sender = await funcs.search_nation(ctx, str(ctx.author.id))
        except NationNotFoundError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not linked so I couldn't verify your bank permissions!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        try:
            if not await perms.check_bank_perms(
                nation=sender, author=ctx.author, action="send"
            ):
                await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to send money from your alliance bank!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
                return
        except IndexError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Your alliance hasn't configured this command!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        except AttributeError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance so you can't send money!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        if len(resources) == 0:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't give any valid resources!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
            return
        if ctx.guild is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This command isn't publicly available yet! If you want it bug Village for it!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if ctx.guild.id not in {239076753065115648, 654109011473596417}:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This command isn't publicly available yet! If you want it bug Village for it!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        embed = (
            funcs.get_embed_author_guild(
                author,
                f"Are you sure you want to transfer {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**? To confirm please type the id of the **{type(recipient).__name__}**.",
                color=discord.Color.orange(),
            )
            if isinstance(author, discord.Guild)
            else funcs.get_embed_author_member(
                author,
                f"Are you sure you want to transfer {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**? To confirm please type the id of the **{type(recipient).__name__}**.",
                color=discord.Color.orange(),
            )
        )
        view = Confirm(defer=True)
        message = await ctx.reply(
            embed=embed, view=view, ephemeral=True, return_message=True
        )

        r = await view.wait()
        if r:
            return await message.edit(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't confirm the transaction in time!",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        if not view.value:
            return await message.edit(
                embed=funcs.get_embed_author_guild(
                    author,
                    f"You have cancelled the transfer of {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.red(),
                )
                if isinstance(author, discord.Guild)
                else funcs.get_embed_author_member(
                    author,
                    f"You have cancelled the transfer of {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.red(),
                ),
                view=None,
            )

        message = await message.edit(
            embed=funcs.get_embed_author_guild(
                author,
                f"Sending {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**...",
                color=discord.Color.orange(),
            )
            if isinstance(author, discord.Guild)
            else funcs.get_embed_author_member(
                author,
                f"Sending {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**...",
                color=discord.Color.orange(),
            ),
            view=None,
        )

        complete = await resources.complete(receiver=recipient, action="send")
        if not complete:
            complete = await resources.complete(receiver=recipient, action="send")
            if not complete:
                embed = (
                    funcs.get_embed_author_guild(
                        author,
                        "Something went wrong with the transaction. Please try again.",
                        color=discord.Color.red(),
                    )
                    if isinstance(author, discord.Guild)
                    else funcs.get_embed_author_member(
                        author,
                        "Something went wrong with the transaction. Please try again.",
                        color=discord.Color.red(),
                    )
                )

            else:
                embed = (
                    funcs.get_embed_author_guild(
                        author,
                        f"You successfully transferred {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                        color=discord.Color.green(),
                    )
                    if isinstance(author, discord.Guild)
                    else funcs.get_embed_author_member(
                        author,
                        f"You successfully transferred {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                        color=discord.Color.green(),
                    )
                )

        else:
            embed = (
                funcs.get_embed_author_guild(
                    author,
                    f"You successfully transferred {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.green(),
                )
                if isinstance(author, discord.Guild)
                else funcs.get_embed_author_member(
                    author,
                    f"You successfully transferred {resources} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.green(),
                )
            )

        await message.edit(embed=embed)

    @bank.command(
        name="balance",
        aliases=["bal"],
        brief="Check the balance of an alliance bank.",
        type=commands.CommandType.chat_input,
        descriptions={
            "alliance": "The alliance to check the balance of, defaults to your alliance.",
        },
    )
    async def bank_balance(self, ctx: commands.Context, *, alliance: Alliance = None):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        try:
            viewer = await funcs.search_nation(ctx, str(ctx.author.id))
        except NationNotFoundError:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not linked so I couldn't verify your bank permissions!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        try:
            if not await perms.check_bank_perms(
                nation=viewer, author=ctx.author, action="view"
            ):
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to view your alliance bank!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        except IndexError:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Your alliance hasn't configured this command!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        except AttributeError:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance so you can't view a bank balance!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if ctx.guild is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This command isn't publicly available yet! If you want it bug Village for it!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if ctx.guild.id not in {239076753065115648, 654109011473596417}:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "This command isn't publicly available yet! If you want it bug Village for it!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Fetching the current bank holdings of {repr(alliance)}...",
                color=discord.Color.orange(),
            ),
            return_message=True,
        )
        resources = await alliance.get_resources()
        await message.edit(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The current bank holdings of {repr(alliance)} is:\n{resources.newline()}",
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Bank(bot))
