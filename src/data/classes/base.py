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
    async def fetch(cls) -> Fetchable:
        ...


class Defaultable(Base, metaclass=ABCMeta):
    @abstractclassmethod
    def default(cls) -> Defaultable:
        ...


class Setable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def set_(self, **kwargs: Mapping[str, Any]) -> Setable:
        ...


class Embedable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def get_info_embed(self, ctx: Context) -> Embed:
        ...


class Initable(Base, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        ...


class Saveable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def save(self) -> None:
        ...


class Convertable(Base, metaclass=ABCMeta):
    @abstractclassmethod
    async def convert(self, ctx: Context, argument: str) -> Convertable:
        ...


class Createable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def create(self) -> Createable:
        ...


class ClassCreateable(Base, metaclass=ABCMeta):
    @abstractclassmethod
    async def create(self) -> ClassCreateable:
        ...


class Deleteable(Base, metaclass=ABCMeta):
    @abstractmethod
    async def delete(self) -> None:
        ...
