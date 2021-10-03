from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..db import execute_query, execute_read_query

__all__ = (
    "query_links",
    "add_link",
    "remove_link_user",
    "remove_link_nation",
    "query_link_user",
    "query_link_nation",
)

if TYPE_CHECKING:
    from _typings import LinkData


async def query_links() -> List[LinkData]:
    return await execute_read_query("SELECT * FROM links;")


async def add_link(user_id: int, nation_id: int, /) -> None:
    await execute_query(
        "INSERT INTO links VALUES ($1, $2);",
        user_id,
        nation_id,
    )


async def remove_link_user(user_id: int, /) -> None:
    await execute_query(
        "DELETE FROM links WHERE user_id = $1;",
        user_id,
    )


async def remove_link_nation(nation_id: int, /) -> None:
    await execute_query("DELETE FROM links WHERE nation_id = $1;", nation_id)


async def query_link_user(user_id: int, /) -> List[LinkData]:
    return await execute_read_query("SELECT * FROM links WHERE user_id = $1;", user_id)


async def query_link_nation(nation_id: int, /) -> List[LinkData]:
    return await execute_read_query(
        "SELECT * FROM links WHERE nation_id = $1;", nation_id
    )
