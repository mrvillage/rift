from __future__ import annotations

from typing import Dict, List

from ..db import execute_query, execute_read_query

__all__ = (
    "query_links",
    "add_link",
    "remove_link_user",
    "remove_link_nation",
    "query_link_user",
    "query_link_nation",
)


async def query_links() -> List[Dict[str, int]]:
    return [
        dict(i)
        for i in await execute_read_query(
            """
        SELECT * FROM links;
    """
        )
    ]


async def add_link(user_id: int, nation_id: int, /) -> None:
    await execute_query(
        f"""
        INSERT INTO links
        VALUES
        ({user_id},{nation_id})
    """
    )


async def remove_link_user(user_id: int, /) -> None:
    await execute_query(
        f"""
        DELETE FROM links
        WHERE user_id = {user_id};
    """
    )


async def remove_link_nation(nation_id: int, /) -> None:
    await execute_query(
        f"""
        DELETE FROM links
        WHERE nation_id = {nation_id};
    """
    )


async def query_link_user(user_id: int, /) -> List[Dict[str, int]]:
    return [
        dict(i)
        for i in await execute_read_query(
            f"""
        SELECT * FROM links
        WHERE user_id = {user_id};
    """
        )
    ]


async def query_link_nation(nation_id: int, /) -> List[Dict[str, int]]:
    return [
        dict(i)
        for i in await execute_read_query(
            f"""
        SELECT * FROM links
        WHERE nation_id = {nation_id};
    """
        )
    ]
