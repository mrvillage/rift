from typing import Tuple, Union

from discord import PartialEmoji
from discord.emoji import Emoji

from .base import BaseFlagConverter


class ButtonFlags(BaseFlagConverter):
    action: str
    url: str
    disabled: bool
    style: str
    color: str
    label: str
    name: str
    emoji: Union[PartialEmoji, Emoji]
    options: Tuple[str, ...]


class SelectFlags(BaseFlagConverter):
    placeholder: str
    min_values: int
    max_values: int


class SelectOptionFlags(BaseFlagConverter):
    default: str
    description: str
    emoji: Union[PartialEmoji, Emoji]
    label: str
    action: str
    options: Tuple[str, ...]
