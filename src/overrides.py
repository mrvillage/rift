from __future__ import annotations

import inspect
from typing import Any

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
        return await convert_bool(argument)

    if converter is int or converter is float:
        try:
            return await convert_number(argument)
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
                return await converter().convert(ctx, argument)  # type: ignore
        elif isinstance(converter, Converter):
            return await converter.convert(ctx, argument)  # type: ignore
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


def override():
    converter._actual_conversion = _actual_conversion
