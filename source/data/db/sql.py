from .connect import connection


async def execute_query(query, *args):
    await connection.execute(query, *args)


async def execute_read_query(query, *args):
    return await connection.fetch(query, *args)


async def execute_query_script(query, *args):
    await connection.execute(query, *args)


async def execute_query_no_commit(query, *args):
    await connection.execute(query, *args)


async def execute_read_query_no_commit(query, *args):
    return await connection.fetch(query, *args)


async def execute_query_many(query, iterable):
    await connection.executemany(query, iterable)
