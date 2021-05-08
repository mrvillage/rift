from ..db import execute_query, execute_read_query
from ... import cache


async def get_alliance(search):
    alliance = await execute_read_query("SELECT * FROM alliances WHERE LOWER(name) = LOWER($1);", search)
    if alliance:
        return cache.alliances[alliance[0][0]]
    alliance = await execute_read_query("SELECT * FROM alliances WHERE LOWER(acronym) = LOWER($1);", search)
    if alliance:
        return cache.alliances[alliance[0][0]]
