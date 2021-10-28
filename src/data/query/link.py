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
    from _typings import UserData


async def query_links() -> List[UserData]:
    return await execute_read_query("SELECT * FROM users;")


async def add_link(user_id: int, nation_id: int, /) -> None:
    await execute_query(
        "INSERT INTO users (user_id, nation_id) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET nation_id = $2 WHERE users.user_id = $1;",
        user_id,
        nation_id,
    )


async def remove_link_user(user_id: int, /) -> None:
    await execute_query(
        "UPDATE users SET nation_id = $1 WHERE user_id = $2;",
        None,
        user_id,
    )


async def remove_link_nation(nation_id: int, /) -> None:
    await execute_query(
        "UPDATE users SET nation_id = $1 WHERE nation_id = $2;", None, nation_id
    )


async def query_link_user(user_id: int, /) -> List[UserData]:
    return await execute_read_query("SELECT * FROM users WHERE user_id = $1;", user_id)


async def query_link_nation(nation_id: int, /) -> List[UserData]:
    return await execute_read_query(
        "SELECT * FROM users WHERE nation_id = $1;", nation_id
    )
