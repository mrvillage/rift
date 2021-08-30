from __future__ import annotations

from typing import Dict, List

from ..query import link

__all__ = (
    "get_links",
    "add_link",
    "remove_link_user",
    "remove_link_nation",
    "get_link_user",
    "get_link_nation",
)


async def get_links() -> List[Dict[str, int]]:
    return await link.query_links()


async def add_link(user_id: int, nation_id: int, /) -> None:
    await link.add_link(user_id, nation_id)


async def remove_link_user(user_id: int, /) -> None:
    await link.remove_link_user(user_id)


async def remove_link_nation(nation_id: int, /) -> None:
    await link.remove_link_nation(nation_id)


async def get_link_user(user_id: int, /) -> Dict[str, int]:
    return (await link.query_link_user(user_id))[0]


async def get_link_nation(nation_id: int, /) -> Dict[str, int]:
    return (await link.query_link_nation(nation_id))[0]
