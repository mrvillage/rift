from __future__ import annotations

from typing import List

from _typings import LinkData

from ...cache import cache
from ..query import link

__all__ = (
    "get_links",
    "add_link",
    "remove_link_user",
    "remove_link_nation",
    "get_link_user",
    "get_link_nation",
)


async def get_links() -> List[LinkData]:
    return cache._links


async def add_link(user_id: int, nation_id: int, /) -> None:
    cache._links.append({"user_id": user_id, "nation_id": nation_id})
    await link.add_link(user_id, nation_id)


async def remove_link_user(user_id: int, /) -> None:
    try:
        cache._links.remove(next(i for i in cache._links if i["user_id"] == user_id))
    except StopIteration:
        pass
    await link.remove_link_user(user_id)


async def remove_link_nation(nation_id: int, /) -> None:
    try:
        cache._links.remove(
            next(i for i in cache._links if i["nation_id"] == nation_id)
        )
    except StopIteration:
        pass
    await link.remove_link_nation(nation_id)


async def get_link_user(user_id: int, /) -> LinkData:
    try:
        return next(i for i in cache._links if i["user_id"] == user_id)
    except StopIteration:
        raise IndexError


async def get_link_nation(nation_id: int, /) -> LinkData:
    try:
        return next(i for i in cache._links if i["nation_id"] == nation_id)
    except StopIteration:
        raise IndexError
