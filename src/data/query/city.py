from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..db import execute_read_query

__all__ = ("query_cities", "query_nation_cities")

if TYPE_CHECKING:
    from _typings import CityData


async def query_cities() -> List[CityData]:
    return await execute_read_query("SELECT * FROM cities;")


async def query_nation_cities(nation_id: int) -> List[CityData]:
    return await execute_read_query(
        "SELECT * FROM cities WHERE nation_id = $1;", nation_id
    )
