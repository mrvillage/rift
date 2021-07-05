from ..db.sql import execute_query, execute_read_query


async def get_bot_staff():
    return [i[0] for i in await execute_read_query("SELECT * FROM staff;")]


async def add_bot_staff(user_id):
    await execute_query("INSERT INTO staff VALUES ($1);", user_id)
