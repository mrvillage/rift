from __future__ import annotations

from typing import TypeVar, Union

from discord.embeds import _EmptyEmbed  # type: ignore

__all__ = ("MaybeEmptyEmbed",)

T = TypeVar("T")

MaybeEmptyEmbed = Union[T, _EmptyEmbed]
