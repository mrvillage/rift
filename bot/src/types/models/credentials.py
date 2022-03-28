from __future__ import annotations

from typing import TypedDict

__all__ = ("Credentials",)


class Credentials(TypedDict):
    nation_id: int
    api_key: str
