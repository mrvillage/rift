from __future__ import annotations

from src.cache import cache  # type: ignore

from . import alliances, nations, users

__all__ = ("init_cache",)


def init_cache() -> None:
    cache._alliances = alliances.DATA
    cache._nations = nations.DATA
    cache._users = users.DATA
