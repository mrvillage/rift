from ..db import execute_read_query


async def get_nation(search):
    from ..classes import Nation

    nation = await execute_read_query(
        "SELECT * FROM nations WHERE LOWER(nation) = LOWER($1);", search
    )
    if nation:
        return await Nation.fetch(nation[0][0])
    nation = await execute_read_query(
        "SELECT * FROM nations WHERE LOWER(leader) = LOWER($1);", search
    )
    if nation:
        return await Nation.fetch(nation[0][0])
