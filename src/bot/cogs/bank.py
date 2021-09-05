from asyncio import TimeoutError

import discord
from discord.ext import commands

from ... import find
from ... import funcs
from ... import perms
from ...data.classes.bank import Transaction
from ...errors import AllianceNotFoundError, NationNotFoundError, RecipientNotFoundError
from ...ref import Rift


class Bank(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="bank",
        help="A group of commands related to your alliance bank.",
        invoke_without_command=True,
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def bank(self, ctx: commands.Context):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author, "You forgot to give an argument!"
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
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def bank_transfer(
        self, ctx: commands.Context, recipient, *, transaction: Transaction
    ):
        try:
            author, recipient = await find.search_nation_author(ctx, recipient)
        except NationNotFoundError:
            try:
                recipient = await funcs.search_alliance(ctx, recipient)
                author = ctx.guild
            except AllianceNotFoundError:
                await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"I couldn't find a nation or alliance with argument `{recipient}`.",
                    )
                )
                return
        try:
            sender = await funcs.search_nation(ctx, str(ctx.author.id))
        except NationNotFoundError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not linked so I couldn't verify your bank permissions!",
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
                    )
                )
                return
        except IndexError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "Your alliance hasn't configured this command!"
                )
            )
            return
        except AttributeError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You're not in an alliance so you can't send money!"
                )
            )
            return
        if len(transaction) == 0:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You didn't give any valid resources!"
                )
            )
            return
        embed = (
            funcs.get_embed_author_guild(
                author,
                f"Are you sure you want to transfer {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**? To confirm please type the id of the **{type(recipient).__name__}**.",
            )
            if isinstance(author, discord.Guild)
            else funcs.get_embed_author_member(
                author,
                f"Are you sure you want to transfer {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**? To confirm please type the id of the **{type(recipient).__name__}**.",
            )
        )
        message = await ctx.reply(embed=embed, return_message=True)

        def check(msg: discord.Message):
            return (
                (
                    msg.content == str(recipient.id)
                    or msg.content.lower() in ("c", "cancel")
                )
                and ctx.author.id == msg.author.id
                and ctx.channel.id == msg.channel.id
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except TimeoutError:
            await message.edit(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You didn't confirm your transaction in time!"
                )
            )
            return
        if msg.content in ("c", "cancel"):
            await message.edit(
                embed=funcs.get_embed_author_guild(
                    author,
                    f"You have cancelled the transfer of {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                )
                if isinstance(author, discord.Guild)
                else funcs.get_embed_author_member(
                    author,
                    f"You have cancelled the transfer of {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                )
            )
            return
        message = await message.edit(
            embed=funcs.get_embed_author_guild(
                author,
                f"Sending {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**...",
            )
            if isinstance(author, discord.Guild)
            else funcs.get_embed_author_member(
                author,
                f"Sending {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**...",
            ),
        )
        complete = await transaction.complete(receiver=recipient, action="send")
        if not complete:
            complete = await transaction.complete(receiver=recipient, action="send")
            if not complete:
                embed = (
                    funcs.get_embed_author_guild(
                        author,
                        f"Something went wrong with the transaction. Please try again.",
                    )
                    if isinstance(author, discord.Guild)
                    else funcs.get_embed_author_member(
                        author,
                        f"Something went wrong with the transaction. Please try again.",
                    )
                )
                await message.edit(embed=embed)
            else:
                embed = (
                    funcs.get_embed_author_guild(
                        author,
                        f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    )
                    if isinstance(author, discord.Guild)
                    else funcs.get_embed_author_member(
                        author,
                        f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                    )
                )
                await message.edit(embed=embed)
        else:
            embed = (
                funcs.get_embed_author_guild(
                    author,
                    f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                )
                if isinstance(author, discord.Guild)
                else funcs.get_embed_author_member(
                    author,
                    f"You successfully transferred {str(transaction)} to the **{type(recipient).__name__}** of **{repr(recipient)}**.",
                )
            )
            await message.edit(embed=embed)

    @bank.command(
        name="balance",
        aliases=["bal"],
        help="Send money from your alliance bank.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def bank_balance(self, ctx: commands.Context, *, search=None):
        search = str(ctx.author.id) if search is None else search
        try:
            nation = await funcs.search_nation(ctx, search)
            await nation.make_attrs("alliance")
            alliance = nation.alliance
        except NationNotFoundError:
            try:
                alliance = funcs.search_alliance(ctx, search)
            except AllianceNotFoundError:
                await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"I couldn't find a nation or alliance with argument `{search}`.",
                    )
                )
                raise RecipientNotFoundError
        try:
            viewer = await funcs.search_nation(ctx, str(ctx.author.id))
        except NationNotFoundError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not linked so I couldn't verify your bank permissions!",
                )
            )
            return
        try:
            if not await perms.check_bank_perms(
                nation=viewer, author=ctx.author, action="view"
            ):
                await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "You don't have permission to view your alliance bank!",
                    )
                )
                return
        except IndexError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "Your alliance hasn't configured this command!"
                )
            )
            return
        except AttributeError:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You're not in an alliance so you can't view a bank balance!",
                )
            )
            return
        message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author, f"Fetching the current bank holdings of {repr(alliance)}..."
            )
        )
        resources = await alliance.get_resources()
        await message.edit(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The current bank holdings of {repr(alliance)} is:\n{resources.newline()}",
            )
        )


def setup(bot: Rift):
    bot.add_cog(Bank(bot))
