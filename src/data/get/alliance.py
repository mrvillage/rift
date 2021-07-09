from ..db import execute_read_query


async def get_alliance(search):
    from ..classes.alliance import Alliance

    alliance = await execute_read_query(
        "SELECT * FROM alliances WHERE LOWER(name) = LOWER($1);", search
    )
    if alliance:
        return await Alliance.fetch(alliance[0][0])
    alliance = await execute_read_query(
        "SELECT * FROM alliances WHERE LOWER(acronym) = LOWER($1);", search
    )
    if alliance:
        return await Alliance.fetch(alliance[0][0])
