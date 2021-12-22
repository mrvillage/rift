from __future__ import annotations

import io
import sys
import traceback
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ..data.classes import Alliance, Nation
from ..errors import (
    AccountNotFoundError,
    AllianceNotFoundError,
    EmbassyConfigNotFoundError,
    EmbassyNotFoundError,
    InvalidConditionError,
    MenuItemNotFoundError,
    MenuNotFoundError,
    NationNotFoundError,
    NationOrAllianceNotFoundError,
    NoCredentialsError,
    NoRolesError,
    RoleNotFoundError,
    SubscriptionNotFoundError,
    TargetNotFoundError,
    TicketConfigNotFoundError,
    TicketNotFoundError,
    TransactionNotFoundError,
)
from ..ref import RiftContext
from .embeds import get_embed_author_member
from .utils import get_command_signature

__all__ = ("print_handler", "handler")


async def print_handler(ctx: RiftContext, error: Exception) -> None:
    if hasattr(ctx.command, "on_error"):
        return
    print(
        "Ignoring exception in command {}:".format(ctx.command),
        file=sys.stderr,
        flush=True,
    )
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    sys.stderr.flush()
    f = io.StringIO()
    traceback.print_exception(type(error), error, error.__traceback__, file=f)
    channel = ctx.bot.get_channel(919428590167277609)
    if channel is not None:
        if TYPE_CHECKING:
            assert isinstance(channel, discord.TextChannel)
        try:
            await channel.send(
                embed=get_embed_author_member(
                    ctx.author,
                    f"Error encountered by {ctx.author.mention} in guild {ctx.guild and ctx.guild.name} ({ctx.guild and ctx.guild.id})\n\n"
                    f"Command: {ctx.command and ctx.command.qualified_name}\n"
                    f"ID: {ctx.message.id if ctx.message else ctx.interaction.id}\n\n"
                    f"```py\n{f.getvalue()}\n```",
                    color=discord.Color.red(),
                )
            )
        except discord.HTTPException:
            print(
                "Failed to send error message to errors channel.",
                file=sys.stderr,
                flush=True,
            )


async def handler(ctx: RiftContext, error: Exception) -> None:
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
                    f"You forgot an argument!\n\n`{get_command_signature(ctx)}`",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, commands.MissingPermissions):
            if error.missing_permissions[0] == "manage":
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You need to have the `Manage Server` or `Administrator` permission or have a manager role to run this command.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            elif error.missing_permissions[0] == "manage_no_role":
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You need to have the `Manage Server` or `Administrator` to run this command.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            elif error.missing_permissions[0] == "alliance_manage":
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You need to have permission to manage your alliance's settings to run this command.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            elif error.missing_permissions[0] == "alliance_manage_roles":
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You don't have permission to manage that alliance's roles!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
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
                ),
                ephemeral=True,
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"You gave an invalid argument!\n\n`{get_command_signature(ctx)}`",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "You can't use that command in DMs! Try it in a server instead.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "You can't use that command in a server! Try it in DMs instead.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, NoCredentialsError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "I don't have any valid credentials to perform that action!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, NoRolesError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"You don't have any roles to allow you to perform that action on alliance {repr(error.args[0])}!\nRequired Permissions: {', '.join(f'`{i}`' for i in error.args[1:]) if error.args[1:] else 'None'}",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, NationNotFoundError):
            if str(error.args[0]) == str(ctx.author.id) or error.args[0] is None:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You're not linked so I can't infer your nation!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            else:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        f"No nation found with argument `{error.args[0]}`.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        elif isinstance(error, AllianceNotFoundError):
            if str(error.args[0]) == str(ctx.author.id) or error.args[0] is None:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You're not linked so I can't infer your alliance!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            else:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        f"No alliance found with argument `{error.args[0]}`.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        elif isinstance(error, MenuNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No menu found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, MenuItemNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No menu item found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, TargetNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No target found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, SubscriptionNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No subscription found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, TicketNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No ticket found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, TicketConfigNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No ticket config found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, EmbassyNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No embassy found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, EmbassyConfigNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No embassy config found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, RoleNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No role found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, AccountNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No account found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, TransactionNotFoundError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"No transaction found with argument `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, InvalidConditionError):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"Invalid condition `{error.args[0]}`.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, commands.BadUnionArgument):
            if (error.converters[0] is Alliance or error.converters[0] is Nation) and (  # type: ignore
                error.converters[1] is Alliance or error.converters[1] is Nation  # type: ignore
            ):
                if error.errors[0].args[1].args[0] == str(ctx.author.id):
                    await ctx.reply(
                        embed=get_embed_author_member(
                            ctx.author,
                            "You're not linked so I can't infer your nation!",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                else:
                    await ctx.reply(
                        embed=get_embed_author_member(
                            ctx.author,
                            f"No nation or alliance found with argument `{error.errors[0].args[1].args[0]}`.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
            else:
                await print_handler(ctx, error)
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Beta, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        elif isinstance(error, discord.NotFound):
            if error.code != 10062:
                await print_handler(ctx, error)
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Beta, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        elif isinstance(error, discord.HTTPException):
            if error.code == 30007:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "Sorry, but I can't add any more subscriptions to this channel, the maximum number of webhooks (10) has been reached! Please try again in a different channel.",
                        color=discord.Color.red(),
                    )
                )
            elif error.code == 50027:
                pass
            else:
                await print_handler(ctx, error)
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Beta, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        elif isinstance(error, NationOrAllianceNotFoundError):
            if error.args[0] == str(ctx.author.id):
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        "You're not linked so I can't infer your nation!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            else:
                await ctx.reply(
                    embed=get_embed_author_member(
                        ctx.author,
                        f"No nation or alliance found with argument `{error.args[0]}`.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        else:
            await print_handler(ctx, error)
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Beta, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
    except discord.Forbidden:
        await ctx.reply(
            'I don\'t have permission to do that! Please make sure I have the "Embed Links" permission.'
        )
    except Exception as e:
        await print_handler(ctx, e)
        await ctx.reply(
            embed=get_embed_author_member(
                ctx.author,
                "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Beta, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                color=discord.Color.red(),
            ),
            ephemeral=True,
        )
