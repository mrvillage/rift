import traceback
import sys
import discord
from discord.ext import commands
from .embeds import get_embed_author_member
from .utils import get_command_signature


async def print_handler(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    cog = ctx.cog
    if cog and commands.Cog._get_overridden_method(cog.cog_command_error) is not None:
        return
    print('Ignoring exception in command {}:'.format(
        ctx.command), file=sys.stderr)
    traceback.print_exception(
        type(error), error, error.__traceback__, file=sys.stderr)


async def handler(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=get_embed_author_member(ctx.author, f"You forgot an argument!\n\n`{await get_command_signature(ctx)}`"))
        elif isinstance(error, discord.Forbidden):
            await ctx.reply(f"I don't have permission to do that! Please make sure I have the \"Embed Links\" permission.")
        else:
            await ctx.reply(embed=get_embed_author_member(ctx.author, f"Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance."))
            await print_handler(ctx, error)
    except discord.Forbidden:
        await ctx.reply(f"I don't have permission to do that! Please make sure I have the \"Embed Links\" permission.")
