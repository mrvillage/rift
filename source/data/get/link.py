from ..db import execute_query, execute_read_query


async def get_links():
    return await execute_read_query("""
        SELECT * FROM links;
    """)


async def add_link(user_id, nation_id):
    return await execute_query(f"""
        INSERT INTO links
        VALUES
        ({user_id},{nation_id})
    """)


async def remove_link_user(user_id):
    return await execute_query(f"""
        DELETE FROM links
        WHERE id = {user_id};
    """)


async def remove_link_nation(nation_id):
    return await execute_query(f"""
        DELETE FROM links
        WHERE nation = {nation_id};
    """)


async def get_link_user(user_id):
    return (await execute_read_query(f"""
        SELECT * FROM links
        WHERE id = {user_id};
    """))[0]


async def get_link_nation(nation_id):
    return (await execute_read_query(f"""
        SELECT * FROM links
        WHERE nation = {nation_id};
    """))[0]
