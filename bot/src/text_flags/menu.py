from typing import Optional, Tuple, Union

from discord import PartialEmoji
from discord.emoji import Emoji
from discord.ext.commands.flags import flag

from .base import BaseFlagConverter


class ButtonFlags(BaseFlagConverter, case_insensitive=True):
    action: Optional[str]
    url: Optional[str]
    disabled: Optional[bool] = flag(default=False)
    style: Optional[str] = flag(aliases=["color"], default=2)
    label: Optional[str] = flag(aliases=["name"])
    emoji: Optional[Union[PartialEmoji, Emoji]]
    options: Optional[Tuple[str, ...]]
    row: Optional[int]
    id: Optional[int]
    patch: Optional[str]


class SelectFlags(BaseFlagConverter, case_insensitive=True):
    placeholder: Optional[str]
    min_values: Optional[int] = flag(default=1)
    max_values: Optional[int] = flag(default=1)
    id: Optional[int]
    row: Optional[int]


class SelectOptionFlags(BaseFlagConverter, case_insensitive=True):
    default: Optional[bool] = flag(default=False)
    description: Optional[str]
    emoji: Optional[Union[PartialEmoji, Emoji]]
    label: str = flag(aliases=["name"])
    action: Optional[str]
    options: Optional[Tuple[str, ...]]
    row: Optional[int]
