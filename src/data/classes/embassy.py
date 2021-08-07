from __future__ import annotations

from discord.ext import commands

from .base import Convertable, Fetchable, Initable, Saveable


class Embassy(Convertable, Fetchable, Initable, Saveable):
    def __init__(self) -> None:
        ...

    @classmethod
    async def fetch(cls, guild_id: int, alliance_id: int) -> Embassy:
        ...

    async def save(self) -> None:
        ...

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Embassy:
        ...

    def __int__(self) -> int:
        ...
