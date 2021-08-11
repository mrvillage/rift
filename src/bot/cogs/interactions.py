from __future__ import annotations

import inspect
from typing import Any, Coroutine, Dict, List, Union

import discord
from discord.ext.commands.converter import _actual_conversion
from discord.ext import commands

from ... import funcs
from ...ref import Rift


class InteractionContext(commands.Context):
    interaction: discord.Interaction

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.interaction = kwargs["interaction"]
        self.author = self.interaction.user  # type: ignore
        self.guild = self.interaction.guild  # type: ignore
        self.channel = self.interaction.channel  # type: ignore
        self.followup = self.interaction.followup
        self.send = self.followup.send  # type: ignore

    async def reply(self, *args, **kwargs) -> discord.Message:
        if args:
            kwargs["content"] = args[0]
        await self.interaction.edit_original_message(**kwargs)
        return await self.interaction.original_message()


class FakeParam(inspect.Parameter):
    def __init__(self, name: str) -> None:
        self.__dict__["name"] = name


async def parse_arguments(
    ctx: InteractionContext,
    coro: Coroutine[Any, Any, Any],
    options: List[Dict[str, Any]],
) -> None:
    for option in options:
        name = option["name"]
        value = option["value"]
        if option["type"] in {1, 2, 4, 5, 10}:
            ctx.args.append(value)
            ctx.kwargs[name] = value
            continue
        conv = coro.__annotations__.get(option["name"], None)
        if conv is None:
            ctx.args.append(value)
            ctx.kwargs[name] = value
        elif conv is Union:
            for c in conv.__dict__["__args__"]:
                try:
                    arg = await _actual_conversion(ctx, c, value, FakeParam(name))
                except Exception:
                    continue
                else:
                    ctx.args.append(arg)
                    ctx.kwargs[name] = arg
                    break
            else:
                raise commands.BadArgument(f"Could not parse {value} as {conv}")
        else:
            arg = await _actual_conversion(ctx, conv, value, FakeParam(name))
            ctx.args.append(arg)
            ctx.kwargs[name] = arg


class Interactions(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type is not discord.InteractionType.application_command:
            return
        await interaction.response.defer()
        command: commands.Command = self.bot.get_command(interaction.data["name"])  # type: ignore
        message = await interaction.original_message()
        ctx = InteractionContext(
            interaction=interaction,
            bot=self.bot,
            prefix="/",
            command=command,
            message=message,
        )
        self.bot.dispatch("command", ctx)
        ctx.args = [ctx] if command.cog is None else [command.cog, ctx]
        try:
            if not await command.can_run(ctx):
                raise commands.CheckFailure(
                    f"The check functions for command {command.qualified_name} failed."
                )
        except commands.CommandError as error:
            await command.dispatch_error(ctx, error)
        if command._max_concurrency is not None:
            await command._max_concurrency.acquire(ctx)
        try:
            if command.cooldown_after_parsing:
                await parse_arguments(
                    ctx, command._callback, interaction.data.get("options", [])  # type: ignore
                )
                command._prepare_cooldowns(ctx)
            else:
                command._prepare_cooldowns(ctx)
                await parse_arguments(
                    ctx, command._callback, interaction.data.get("options", [])  # type: ignore
                )
            await command.call_before_hooks(ctx)
        except Exception as error:
            if command._max_concurrency is not None:
                await command._max_concurrency.release(ctx)
            return await command.dispatch_error(ctx, error)
        try:
            await ctx.invoke(command, **ctx.kwargs)
        except Exception as error:
            await command.dispatch_error(ctx, error)
        else:
            self.bot.dispatch("command_completion", ctx)


def setup(bot: Rift) -> None:
    bot.add_cog(Interactions(bot))
