from __future__ import annotations

from discord.ext import commands

from .base import Convertable, Fetchable, Initable, Saveable


class Ticket(Convertable, Fetchable, Initable, Saveable):
    def __init__(self) -> None:
        ...

    @classmethod
    async def fetch(cls, guild_id: int, alliance_id: int) -> Ticket:
        ...

    async def save(self) -> None:
        ...

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Ticket:
        ...

    def __int__(self) -> int:
        ...
