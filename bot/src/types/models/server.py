from __future__ import annotations

from typing import TypedDict

__all__ = ("Server",)


class Server(TypedDict):
    id: int
    guild_id: int
    name: str
    invite: str
    description: str
    tags: list[str]
