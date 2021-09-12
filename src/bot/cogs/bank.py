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
        help="A group of commands related to your alliance bank.",
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    async def bank(self, ctx: commands.Context):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author, "You forgot to give an argument!", color=discord.Color.red()
            )
        )

    @commands.command(
        name="send", help="Send money from your alliance bank.", hidden=True
    )
    async def send(self, ctx: commands.Context, recipient, *, transaction: Transaction):
        await ctx.invoke(self.bank_transfer, recipient, transaction=transaction)

    @bank.command(
        name="transfer",
        aliases=["send"],
        help="Send money from your alliance bank.",
        type=commands.CommandType.chat_input,
    )
    async def bank_transfer(
        self,
        ctx: commands.Context,
        recipient: Union[Alliance, Nation],
        *,
        transaction: Transaction,
    ):
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
                )
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
                    )
                )
                return
        except IndexError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Your alliance hasn't configured this command!",
                    color=discord.Color.red(),
                )
            )
            return
        except AttributeError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance so you can't send money!",
                    color=discord.Color.red(),
                )
            )
            return
        if len(transaction) == 0:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't give any valid resources!",
                    color=discord.Color.red(),
                )
            )
            return
        embed = (
            funcs.get_embed_author_guild(
                author,
                f"Are you sure you want to transfer {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**? To confirm please type the id of the **{type(recipient).__name__}**.",
                color=discord.Color.orange(),
            )
            if isinstance(author, discord.Guild)
            else funcs.get_embed_author_member(
                author,
                f"Are you sure you want to transfer {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**? To confirm please type the id of the **{type(recipient).__name__}**.",
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
                    f"You have cancelled the transfer of {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.red(),
                )
                if isinstance(author, discord.Guild)
                else funcs.get_embed_author_member(
                    author,
                    f"You have cancelled the transfer of {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.red(),
                ),
                view=None,
            )
        message = await message.edit(
            embed=funcs.get_embed_author_guild(
                author,
                f"Sending {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**...",
                color=discord.Color.orange(),
            )
            if isinstance(author, discord.Guild)
            else funcs.get_embed_author_member(
                author,
                f"Sending {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**...",
                color=discord.Color.orange(),
            ),
            view=None,
        )
        complete = await transaction.complete(receiver=recipient, action="send")
        if not complete:
            complete = await transaction.complete(receiver=recipient, action="send")
            if not complete:
                embed = (
                    funcs.get_embed_author_guild(
                        author,
                        f"Something went wrong with the transaction. Please try again.",
                        color=discord.Color.red(),
                    )
                    if isinstance(author, discord.Guild)
                    else funcs.get_embed_author_member(
                        author,
                        f"Something went wrong with the transaction. Please try again.",
                        color=discord.Color.red(),
                    )
                )
            else:
                embed = (
                    funcs.get_embed_author_guild(
                        author,
                        f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                        color=discord.Color.green(),
                    )
                    if isinstance(author, discord.Guild)
                    else funcs.get_embed_author_member(
                        author,
                        f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                        color=discord.Color.green(),
                    )
                )
        else:
            embed = (
                funcs.get_embed_author_guild(
                    author,
                    f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.green(),
                )
                if isinstance(author, discord.Guild)
                else funcs.get_embed_author_member(
                    author,
                    f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    color=discord.Color.green(),
                )
            )

        await message.edit(embed=embed)

    @bank.command(
        name="balance",
        aliases=["bal"],
        help="Send money from your alliance bank.",
        type=commands.CommandType.chat_input,
    )
    async def bank_balance(self, ctx: commands.Context, *, search=None):
        search = str(ctx.author.id) if search is None else search
        try:
            nation = await funcs.search_nation(ctx, search)
            await nation.make_attrs("alliance")
            alliance = nation.alliance
        except NationNotFoundError:
            try:
                alliance = await funcs.search_alliance(ctx, search)
            except AllianceNotFoundError:
                await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"I couldn't find a nation or alliance with argument `{search}`.",
                        color=discord.Color.red(),
                    )
                )
                raise RecipientNotFoundError
        try:
            viewer = await funcs.search_nation(ctx, str(ctx.author.id))
        except NationNotFoundError:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not linked so I couldn't verify your bank permissions!",
                    color=discord.Color.red(),
                )
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
                    )
                )
        except IndexError:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Your alliance hasn't configured this command!",
                    color=discord.Color.red(),
                )
            )
        except AttributeError:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance so you can't view a bank balance!",
                    color=discord.Color.red(),
                )
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
