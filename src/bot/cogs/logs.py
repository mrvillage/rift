from __future__ import annotations

import json

from discord.ext import commands

from ... import logs
from ...ref import Rift, RiftContext


class Logs(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: RiftContext):
        if ctx.interaction:
            return await logs.insert_log(
                "Unknown",
                ctx.interaction.id,
                ctx.channel.id,
                ctx.guild and ctx.guild.id,
                ctx.author.id,
                "",
                ctx.command and ctx.command.qualified_name,  # type: ignore
                json.dumps([str(i) for i in ctx.args]),
                json.dumps({key: value["value"] for key, value in ctx.options}),
            )
        await logs.insert_log(
            str(ctx.message.edited_at or ctx.message.created_at),
            ctx.message.id,
            ctx.channel.id,
            ctx.guild and ctx.guild.id,
            ctx.author.id,
            ctx.message.content,
            ctx.command and ctx.command.qualified_name,  # type: ignore
            json.dumps([str(i) for i in ctx.args]),
            json.dumps({i: str(ctx.kwargs[i]) for i in ctx.kwargs}),
        )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: RiftContext):
        if ctx.interaction:
            return await logs.edit_log(
                "Unknown",
                ctx.interaction.id,
                ctx.channel.id,
                ctx.guild and ctx.guild.id,
                ctx.author.id,
                "",
                ctx.command and ctx.command.qualified_name,  # type: ignore
                True,
            )
        await logs.edit_log(
            str(ctx.message.edited_at or ctx.message.created_at),
            ctx.message.id,
            ctx.channel.id,
            ctx.guild and ctx.guild.id,
            ctx.author.id,
            ctx.message.content,
            ctx.command and ctx.command.qualified_name,  # type: ignore
            True,
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: RiftContext, error: commands.CommandError):
        if ctx.interaction:
            return await logs.edit_log(
                "Unknown",
                ctx.interaction.id,
                ctx.channel.id,
                ctx.guild and ctx.guild.id,
                ctx.author.id,
                "",
                ctx.command and ctx.command.qualified_name,  # type: ignore
                False,
                str(error),
            )
        await logs.edit_log(
            str(ctx.message.edited_at or ctx.message.created_at),
            ctx.message.id,
            ctx.channel.id,
            ctx.guild and ctx.guild.id,
            ctx.author.id,
            ctx.message.content,
            ctx.command and ctx.command.qualified_name,  # type: ignore
            False,
            str(error),
        )


def setup(bot: Rift):
    bot.add_cog(Logs(bot))
