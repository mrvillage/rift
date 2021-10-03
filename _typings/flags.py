from __future__ import annotations

from typing import List, Set, TypedDict, Union

import discord

__all__ = ("MenuFormattedFlags",)


class MenuFormattedFlagsOptional(TypedDict, total=False):
    action: str
    style: str
    options: Union[List[int], Set[int]]
    url: str
    disabled: bool
    label: str
    emoji: Union[discord.Emoji, discord.PartialEmoji]
    row: int
    id: int


class MenuFormattedFlags(MenuFormattedFlagsOptional):
    ...
