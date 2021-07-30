from __future__ import annotations

import inspect
from types import FunctionType
from typing import Any, Dict, List

import discord
from discord.ext import commands
from discord.ext.commands import (
    BadArgument,
    CommandError,
    Context,
    ConversionError,
    Converter,
    converter,
)
from discord.ext.commands.converter import CONVERTER_MAPPING


async def _actual_conversion(
    ctx: Context, converter: Any, argument: str, param: inspect.Parameter
) -> Any:
    from .funcs.utils import convert_bool, convert_number

    if converter is bool:
        return convert_bool(argument)

    if converter is int or converter is float:
        try:
            num = convert_number(argument)
        except Exception as exc:
            try:
                name = converter.__name__
            except AttributeError:
                name = converter.__class__.__name__

            raise BadArgument(
                f'Converting to "{name}" failed for parameter "{param.name}".'
            ) from exc

    try:
        module = converter.__module__
    except AttributeError:
        pass
    else:
        if module is not None and (
            module.startswith("discord.") and not module.endswith("converter")
        ):
            converter = CONVERTER_MAPPING.get(converter, converter)

    try:
        if inspect.isclass(converter) and issubclass(converter, Converter):
            if inspect.ismethod(converter.convert):
                return await converter.convert(ctx, argument)
            else:
                return await converter().convert(ctx, argument)
        elif isinstance(converter, Converter):
            return await converter.convert(ctx, argument)
    except CommandError:
        raise
    except Exception as exc:
        raise ConversionError(converter, exc) from exc

    try:
        return converter(argument)
    except CommandError:
        raise
    except Exception as exc:
        try:
            name = converter.__name__
        except AttributeError:
            name = converter.__class__.__name__

        raise BadArgument(
            f'Converting to "{name}" failed for parameter "{param.name}".'
        ) from exc


class ButtonStyleOverride(discord.ButtonStyle):
    def __get_item__(self, name: str):
        self.__getattribute__(name)


def convert_slash_command_type(type_: type) -> int:
    if type_ is str:
        return 3
    if type_ is int:
        return 4
    if type_ is bool:
        return 5
    if type_ is discord.User:
        return 6
    if (
        type_ is discord.TextChannel
        or type_ is discord.VoiceChannel
        or type_ is discord.CategoryChannel
    ):
        return 7
    if type_ is discord.Role:
        return 8
    if type_ is float:
        return 10


# "<command name>-<argument name>": description
# For slash command argument descriptions
arg_descriptions = {}
# "<command name>-<argument name>": [choices]
# For slash command argument choices
arg_options = {}


def parse_slash_command_args(coro: FunctionType) -> List[Dict[str, Any]]:
    signature = inspect.signature(coro)
    params = [i for i in signature.parameters.values() if i.name not in {"self", "ctx"}]
    options = []
    for param in params:
        option = {
            "name": param.name,
            "description": arg_descriptions.get(
                f"{coro.__name__}-{param.name}",
                coro.__annotations__.get(param.name, str).__name__,
            ),
            "type": convert_slash_command_type(
                coro.__annotations__.get(param.name, str)
            ),
        }
        choices = arg_options.get(f"{coro.__name__}-{param.name}", None)
        if choices:
            option["choices"] = choices
        if not hasattr(param, "default"):
            option["required"] = True
        options.append(option)
    return options


async def register_slash_command(
    command: commands.Command, options: List[Dict[str, Any]]
) -> None:
    from .ref import bot

    bot.global_application_commands.append(
        # await bot.http.upsert_global_command(
        await bot.http.upsert_guild_command(
            bot.application_id,
            654109011473596417,
            {
                "name": command.name,
                "description": command.description or command.name,
                "options": options,  # type: ignore
            },
        )
    )


def _slash(command: commands.Command) -> commands.Command:
    from .ref import bot

    names = [i["name"] for i in bot.global_application_commands]
    args = parse_slash_command_args(command.callback)
    if command.name in names:
        application_command = next(
            i for i in bot.global_application_commands if i["name"] == command.name
        )
        if args == application_command.get("options", []):
            return command
        bot.global_application_commands.remove(application_command)
        bot.loop.create_task(register_slash_command(command, args))
    bot.loop.create_task(register_slash_command(command, args))
    return command


def override():
    converter._actual_conversion = _actual_conversion
    discord.ButtonStyle = ButtonStyleOverride
    commands._slash = _slash  # type: ignore
