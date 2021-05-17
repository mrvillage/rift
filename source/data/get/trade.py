from ..db import execute_read_query


async def get_prices():
    return (await execute_read_query("SELECT * FROM prices ORDER BY datetime DESC LIMIT 1;"))[0]
