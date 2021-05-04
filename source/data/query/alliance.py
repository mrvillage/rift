from ..db import execute_query, execute_read_query, execute_query_many

async def get_applicants(*, alliance_id:int):
    return await execute_read_query("""
        SELECT * FROM alliances
        WHERE alliance_id = $1 AND alliance_position = 1;
    """, alliance_id)

async def get_alliance(*, alliance_id=None, alliance_name=None):
    if alliance_id is not None:
        return (await execute_read_query(f"""
            SELECT * FROM alliances
            WHERE nation_id = {alliance_id};
        """))[0]
    elif alliance_name is not None:
        return (await execute_read_query(f"""
            SELECT * FROM alliances
            WHERE LOWER(alliance) = LOWER({alliance_name});
        """))[0]

async def get_alliances():
    return await execute_read_query("SELECT * FROM alliances;")