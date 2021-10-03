from typing import Any, List, Sequence

from .connect import connection


async def execute_query(query: str, *args: Any) -> None:
    await connection.execute(query, *args)  # type: ignore


async def execute_read_query(query: str, *args: Any) -> List[Any]:
    return await connection.fetch(query, *args)  # type: ignore


async def execute_query_script(query: str, *args: Any) -> None:
    await connection.execute(query, *args)  # type: ignore


async def execute_query_no_commit(query: str, *args: Any) -> None:
    await connection.execute(query, *args)  # type: ignore


async def execute_read_query_no_commit(query: str, *args: Any) -> List[Any]:
    return await connection.fetch(query, *args)  # type: ignore


async def execute_query_many(query: str, iterable: Sequence[List[Any]]):
    await connection.executemany(query, iterable)  # type: ignore
