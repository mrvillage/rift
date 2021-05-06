from ..db import execute_query, execute_read_query


async def get_nation(*, nation_id=None, nation_name=None):
    if nation_id is not None:
        return (await execute_read_query(f"""
            SELECT * FROM nations
            WHERE nation_id = {nation_id};
        """))[0]
    elif nation_name is not None:
        return (await execute_read_query(f"""
            SELECT * FROM nations
            WHERE LOWER(nation) = LOWER({nation_name});
        """))[0]
