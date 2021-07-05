from asyncio import get_event_loop

from asyncpg import create_pool

from ...env import DBHOST, DBNAME, DBPASSWORD, DBPORT, DBUSER


async def _create_connection():
    return await create_pool(
        host=DBHOST, port=DBPORT, user=DBUSER, password=DBPASSWORD, database=DBNAME
    )


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
