from __future__ import annotations

from abc import ABCMeta, abstractclassmethod, abstractmethod
from typing import Any, Mapping
from discord.embeds import Embed

from discord.ext.commands import Context


class Base:
    ...


class Makeable(Base):
    async def make_attrs(self, *attrs):
        for attr in attrs:
            await getattr(self, f"_make_{attr}")()


class Fetchable(Base, metaclass=ABCMeta):
    @abstractclassmethod
    async def fetch(self: Fetchable) -> Fetchable:
        ...


class Defaultable(Base, metaclass=ABCMeta):
    @abstractclassmethod
    def default(self: Defaultable) -> Defaultable:
        ...


class Setable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def set_(self: Setable, **kwargs: Mapping[str, Any]) -> Setable:
        ...


class Embedable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def get_info_embed(self: Embedable, ctx: Context) -> Embed:
        ...


class Initable(Base, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self: Initable) -> None:
        ...
