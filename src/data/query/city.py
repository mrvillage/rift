from ..db import execute_read_query


async def get_city(*, city_id=None, city_name=None):
    pass


async def get_cities():
    return await execute_read_query("SELECT * FROM cities;")
