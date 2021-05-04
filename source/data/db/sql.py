from .connect import connection

# async def execute_query(connection, query):
#     await connection.execute(query)
#     await connection.commit()

# async def execute_read_query(connection, query):
#     cursor = await connection.execute(query)
#     await connection.commit()
#     return await cursor.fetchall()

# async def execute_query_script(connection,query):
#     await connection.executescript(query)
#     await connection.commit()

# async def execute_query_no_commit(connection, query):
#     await connection.execute(query)

# async def execute_read_query_no_commit(connection, query):
#     cursor = await connection.execute(query)
#     return await cursor.fetchall()

# async def execute_query_many(connection,query,iterable):
#     await connection.executemany(query, iterable)
#     await connection.commit()

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

async def execute_query_many(query,iterable):
    await connection.executemany(query, iterable)