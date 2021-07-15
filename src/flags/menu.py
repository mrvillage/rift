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
    label: str = flag(aliases=["name"])
    emoji: Optional[Union[PartialEmoji, Emoji]]
    options: Tuple[str, ...]
    row: Optional[int]
    id: Optional[int]


class SelectFlags(BaseFlagConverter, case_insensitive=True):
    placeholder: Optional[str]
    min_values: Optional[int]
    max_values: Optional[int]
    id: Optional[int]


class SelectOptionFlags(BaseFlagConverter, case_insensitive=True):
    default: bool
    description: str
    emoji: Union[PartialEmoji, Emoji]
    label: str = flag(name="label", aliases=["name"])
    action: str
    options: Tuple[str, ...]
    row: Optional[int]
