from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from ... import funcs
from ...ref import Rift, RiftContext


class Errors(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: RiftContext, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        if TYPE_CHECKING:
            assert ctx.command is not None
        if ctx.command.has_error_handler():
            return
        cog = ctx.cog
        if (
            cog
            and commands.Cog._get_overridden_method(cog.cog_command_error) is not None  # type: ignore
        ):
            return
        await funcs.handler(ctx, error)


def setup(bot: Rift):
    bot.add_cog(Errors(bot))
