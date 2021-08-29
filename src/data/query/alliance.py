from ..db import execute_read_query


async def query_applicants(*, alliance_id: int):
    return await execute_read_query(
        """
        SELECT * FROM nations
        WHERE alliance_id = $1 AND alliance_position = 1;
    """,
        alliance_id,
    )


async def query_members(*, alliance_id: int):
    return await execute_read_query(
        """
        SELECT * FROM nations
        WHERE alliance_id = $1 AND alliance_position != 1;
    """,
        alliance_id,
    )


async def query_alliance(*, alliance_id=None, alliance_name=None):
    if alliance_id is not None:
        return (
            await execute_read_query(
                f"""
            SELECT * FROM alliances
            WHERE id = {alliance_id};
        """
            )
        )[0]
    elif alliance_name is not None:
        return (
            await execute_read_query(
                f"""
            SELECT * FROM alliances
            WHERE LOWER(alliance) = LOWER({alliance_name});
        """
            )
        )[0]


async def query_alliances():
    return await execute_read_query("SELECT * FROM alliances;")
