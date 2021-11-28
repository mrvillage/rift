from __future__ import annotations

from typing import Set

from ...cache import cache
from ...data.classes import User
from ...ref import bot
from ..query import link

__all__ = (
    "get_links",
    "add_link",
    "remove_link_user",
    "remove_link_nation",
    "get_link_user",
    "get_link_nation",
)


async def get_links() -> Set[User]:
    return cache.users


async def add_link(user_id: int, nation_id: int, /) -> None:
    user = User({"user_id": user_id, "nation_id": nation_id})
    cache.add_user(user)
    await link.add_link(user_id, nation_id)
    bot.dispatch("link_create", user)


async def remove_link_user(user_id: int, /) -> None:
    try:
        cache.remove_user(next(i for i in cache.users if i.user_id == user_id))
    except StopIteration:
        pass
    await link.remove_link_user(user_id)


async def remove_link_nation(nation_id: int, /) -> None:
    try:
        cache.remove_user(next(i for i in cache.users if i.nation_id == nation_id))
    except StopIteration:
        pass
    await link.remove_link_nation(nation_id)


async def get_link_user(user_id: int, /) -> User:
    try:
        return next(i for i in cache.users if i.user_id == user_id)
    except StopIteration:
        raise IndexError


async def get_link_nation(nation_id: int, /) -> User:
    try:
        return next(i for i in cache.users if i.nation_id == nation_id)
    except StopIteration:
        raise IndexError
