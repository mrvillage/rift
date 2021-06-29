from asyncpg import create_pool
from asyncio import get_event_loop
from ...env import DBHOST, DBPORT, DBUSER, DBPASSWORD, DBNAME


async def _create_connection():
    return await create_pool(
        host=DBHOST, port=DBPORT, user=DBUSER, password=DBPASSWORD, database=DBNAME
    )


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
