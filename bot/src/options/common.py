from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

__all__ = ("CommonOption",)

if TYPE_CHECKING:
    from enum import EnumMeta
    from typing import Any, Callable, Coroutine, Sequence, TypeVar, Union

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

    OPT = TypeVar("OPT", bound="CommonOption")


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
        attribute: quarrel.Missing[str] = quarrel.MISSING,
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
        self.attribute: str = attribute or name

    def __call__(
        self: OPT,
        type: quarrel.Missing[quarrel.ApplicationCommandOptionType] = quarrel.MISSING,
        name: quarrel.Missing[str] = quarrel.MISSING,
        description: quarrel.Missing[str] = quarrel.MISSING,
        converter: quarrel.Missing[ConverterCCC[OPTS]] = quarrel.MISSING,
        converters: quarrel.Missing[list[ConverterCCC[OPTS]]] = quarrel.MISSING,
        default: OptionDefault[OPTS] = quarrel.MISSING,
        choices: quarrel.Missing[EnumMeta] = quarrel.MISSING,
        channel_types: quarrel.Missing[Sequence[quarrel.ChannelType]] = quarrel.MISSING,
        min_value: quarrel.Missing[float] = quarrel.MISSING,
        max_value: quarrel.Missing[float] = quarrel.MISSING,
        autocomplete: quarrel.Missing[bool] = quarrel.MISSING,
        attribute: quarrel.Missing[str] = quarrel.MISSING,
    ) -> OPT:
        return self.__class__(
            self.type if type is quarrel.MISSING else type,
            self.name if name is quarrel.MISSING else name,
            self.description if description is quarrel.MISSING else description,
            converter,
            self.converters
            if converters is quarrel.MISSING and converter is quarrel.MISSING
            else converters,
            self.default if default is quarrel.MISSING else default,
            self.choices if choices is quarrel.MISSING else choices,
            self.channel_types if channel_types is quarrel.MISSING else channel_types,
            self.min_value if min_value is quarrel.MISSING else min_value,
            self.max_value if max_value is quarrel.MISSING else max_value,
            self.autocomplete if autocomplete is quarrel.MISSING else autocomplete,
            self.attribute if attribute is quarrel.MISSING else attribute,
        )
