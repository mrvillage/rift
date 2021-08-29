from ..db import execute_read_query


async def query_nation(*, nation_id=None, nation_name=None):
    if nation_id is not None:
        return (
            await execute_read_query(
                f"""
            SELECT * FROM nations
            WHERE id = $1;
        """,
                int(nation_id),
            )
        )[0]
    elif nation_name is not None:
        return (
            await execute_read_query(
                f"""
            SELECT * FROM nations
            WHERE LOWER(name) = LOWER($1);
        """,
                str(nation_name),
            )
        )[0]


async def query_nations():
    return await execute_read_query("SELECT * FROM nations;")
