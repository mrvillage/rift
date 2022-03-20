from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

__all__ = ("CommonOption",)

if TYPE_CHECKING:
    from enum import EnumMeta
    from typing import Any, Callable, Coroutine, Sequence, Union

    from quarrel.interactions.command import OPTS

    from ..commands.common import CommonSlashCommand

    ConverterCCC = Union[
        Callable[["CommonSlashCommand[OPTS]", Any], Coroutine[Any, Any, Any]],
        Callable[["CommonSlashCommand[OPTS]", Any], Any],
    ]
    OptionDefault = Union[
        Any,
        Callable[["CommonSlashCommand[OPTS]"], Coroutine[Any, Any, Any]],
        Callable[["CommonSlashCommand[OPTS]"], Any],
    ]


class CommonOption(quarrel.Option):
    def __init__(
        self,
        type: quarrel.ApplicationCommandOptionType,
        name: str,
        description: str,
        converter: quarrel.Missing[ConverterCCC[OPTS]] = quarrel.MISSING,
        converters: quarrel.Missing[list[ConverterCCC[OPTS]]] = quarrel.MISSING,
        default: OptionDefault[OPTS] = quarrel.MISSING,
        choices: quarrel.Missing[EnumMeta] = quarrel.MISSING,
        channel_types: quarrel.Missing[Sequence[quarrel.ChannelType]] = quarrel.MISSING,
        min_value: quarrel.Missing[float] = quarrel.MISSING,
        max_value: quarrel.Missing[float] = quarrel.MISSING,
        autocomplete: quarrel.Missing[bool] = quarrel.MISSING,
    ):
        self.type: quarrel.ApplicationCommandOptionType = type
        self.name: str = name
        self.description: str = description
        if converter is not quarrel.MISSING and converters is not quarrel.MISSING:
            raise ValueError("Only one of converter and converters can be specified")
        self.converters: list[ConverterCCC[OPTS]] = (
            [converter] if converter is not quarrel.MISSING else converters
        ) or []

        self.default: OptionDefault[OPTS] = default
        self.choices: quarrel.Missing[EnumMeta] = choices
        self.channel_types: quarrel.Missing[
            Sequence[quarrel.ChannelType]
        ] = channel_types
        self.min_value: quarrel.Missing[float] = min_value
        self.max_value: quarrel.Missing[float] = max_value
        self.autocomplete: quarrel.Missing[bool] = autocomplete
