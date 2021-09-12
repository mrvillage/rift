from __future__ import annotations

import sys
import traceback

import discord
from discord.ext import commands

from ..errors import AllianceNotFoundError, MenuNotFoundError, NationNotFoundError
from .embeds import get_embed_author_member
from .utils import get_command_signature


async def print_handler(ctx: commands.Context, error: Exception) -> None:
    if hasattr(ctx.command, "on_error"):
        return
    print(
        "Ignoring exception in command {}:".format(ctx.command),
        file=sys.stderr,
        flush=True,
    )
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    sys.stderr.flush()


async def handler(ctx: commands.Context, error: Exception) -> None:
    # sourcery no-metrics
    try:
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.ConversionError):
            error = error.original
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"You forgot an argument!\n\n`{await get_command_signature(ctx)}`",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error, discord.Forbidden):
            await ctx.reply(
                'I don\'t have permission to do that! Please make sure I have the "Embed Links" permission.'
            )
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "I couldn't find that member!",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"You gave an invalid argument!\n\n`{await get_command_signature(ctx)}`",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "You can't use that command in DMs! Try it in a server instead.",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "You can't use that command in a server! Try it in DMs instead.",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error, NationNotFoundError):
            if error.args[0] == str(ctx.author.id):
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You're not linked so I can't infer your alliance!",
                        color=discord.Color.red(),
                    )
                )
            else:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        f"No nation found with argument `{error.args[0]}`.",
                        color=discord.Color.red(),
                    )
                )
        elif isinstance(error, AllianceNotFoundError):
            if error.args[0] == str(ctx.author.id):
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You're not linked so I can't infer your alliance!",
                        color=discord.Color.red(),
                    )
                )
            else:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        f"No alliance found with argument `{error.args[0]}`.",
                        color=discord.Color.red(),
                    )
                )
        elif isinstance(error, MenuNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No menu found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                )
            )
        else:
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Alpha, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                    color=discord.Color.red(),
                )
            )
            await print_handler(ctx, error)
    except discord.Forbidden:
        await ctx.reply(
            'I don\'t have permission to do that! Please make sure I have the "Embed Links" permission.'
        )
    except Exception as e:
        await ctx.reply(
            embed=get_embed_author_member(
                ctx.author,
                "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Alpha, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                color=discord.Color.red(),
            )
        )
        await print_handler(ctx, e)
