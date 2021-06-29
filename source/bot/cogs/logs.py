import json
import discord

from discord.ext import commands

from ... import logs


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if ctx.command is None:
            if hasattr(ctx.message, "edited_at"):
                if ctx.message.edited_at is not None:
                    await logs.insert_log(
                        str(ctx.message.edited_at),
                        ctx.message.id,
                        ctx.channel.id,
                        ctx.guild.id if ctx.guild is not None else None,
                        ctx.author.id,
                        ctx.message.content,
                        None,
                        json.dumps([str(i) for i in ctx.args]),
                        json.dumps({i: str(ctx.kwargs[i]) for i in ctx.kwargs}),
                    )
                    return
            await logs.insert_log(
                str(ctx.message.created_at),
                ctx.message.id,
                ctx.channel.id,
                ctx.guild.id if ctx.guild is not None else None,
                ctx.author.id,
                ctx.message.content,
                ctx.command.qualified_name,
                json.dumps([str(i) for i in ctx.args]),
                json.dumps({i: str(ctx.kwargs[i]) for i in ctx.kwargs}),
            )
            return
        if hasattr(ctx.message, "edited_at"):
            if ctx.message.edited_at is not None:
                await logs.insert_log(
                    str(ctx.message.edited_at),
                    ctx.message.id,
                    ctx.channel.id,
                    ctx.guild.id if ctx.guild is not None else None,
                    ctx.author.id,
                    ctx.message.content,
                    None,
                    json.dumps([str(i) for i in ctx.args]),
                    json.dumps({i: str(ctx.kwargs[i]) for i in ctx.kwargs}),
                )
                return
        await logs.insert_log(
            str(ctx.message.created_at),
            ctx.message.id,
            ctx.channel.id,
            ctx.guild.id if ctx.guild is not None else None,
            ctx.author.id,
            ctx.message.content,
            ctx.command.qualified_name,
            json.dumps([str(i) for i in ctx.args]),
            json.dumps({i: str(ctx.kwargs[i]) for i in ctx.kwargs}),
        )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if hasattr(ctx.message, "edited_at"):
            if ctx.message.edited_at is not None:
                await logs.edit_log(
                    str(ctx.message.edited_at),
                    ctx.message.id,
                    ctx.channel.id,
                    ctx.guild.id if ctx.guild is not None else None,
                    ctx.author.id,
                    ctx.message.content,
                    ctx.command.qualified_name,
                    True,
                )
                return
        await logs.edit_log(
            str(ctx.message.created_at),
            ctx.message.id,
            ctx.channel.id,
            ctx.guild.id if ctx.guild is not None else None,
            ctx.author.id,
            ctx.message.content,
            ctx.command.qualified_name,
            True,
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            if hasattr(ctx.message, "edited_at"):
                if ctx.message.edited_at is not None:
                    await logs.edit_log(
                        str(ctx.message.edited_at),
                        ctx.message.id,
                        ctx.channel.id,
                        ctx.guild.id if ctx.guild is not None else None,
                        ctx.author.id,
                        ctx.message.content,
                        None,
                        False,
                        str(error),
                    )
                    return
            await logs.edit_log(
                str(ctx.message.created_at),
                ctx.message.id,
                ctx.channel.id,
                ctx.guild.id if ctx.guild is not None else None,
                ctx.author.id,
                ctx.message.content,
                None,
                False,
                str(error),
            )
            return
        if hasattr(ctx.message, "edited_at"):
            if ctx.message.edited_at is not None:
                await logs.edit_log(
                    str(ctx.message.edited_at),
                    ctx.message.id,
                    ctx.channel.id,
                    ctx.guild.id if ctx.guild is not None else None,
                    ctx.author.id,
                    ctx.message.content,
                    ctx.command.qualified_name,
                    False,
                    str(error),
                )
                return
        await logs.edit_log(
            str(ctx.message.created_at),
            ctx.message.id,
            ctx.channel.id,
            ctx.guild.id if ctx.guild is not None else None,
            ctx.author.id,
            ctx.message.content,
            ctx.command.qualified_name,
            False,
            str(error),
        )


def setup(bot):
    bot.add_cog(Logs(bot))
