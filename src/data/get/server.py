from ..db import execute_query, execute_read_query


async def add_submit_server(*, invite: str, status: bool, userid: int):
    await execute_query(
        "INSERT INTO serversubmissions (invite, status, userid) VALUES ($1, $2, $3);",
        invite,
        status,
        userid,
    )


async def get_server_submissions():
    return await execute_read_query("SELECT * FROM serversubmissions;")


async def get_server_submissions_pending():
    return await execute_read_query(
        "SELECT * FROM serversubmissions WHERE status is null;"
    )


async def get_server_submissions_approved():
    return await execute_read_query(
        "SELECT * FROM serversubmissions WHERE status = true;"
    )


async def get_server_submissions_denied():
    return await execute_read_query(
        "SELECT * FROM serversubmissions WHERE status = false;"
    )


async def add_server(
    *, name=None, invite=None, categories=None, keywords=None, description=None
):
    await execute_query(
        "INSERT INTO servers (name, invite, categories, keywords, description) VALUES ($1, $2, $3, $4, $5);",
        name,
        invite,
        categories,
        keywords,
        description,
    )


async def edit_server_submission(*, sub_id, status):
    await execute_query(
        "UPDATE serversubmissions SET status = $1 WHERE id = $2;", status, sub_id
    )


async def get_server_ids():
    return [i[0] for i in await execute_read_query("SELECT id FROM servers;")]


async def get_server_submission(*, sub_id):
    return await execute_read_query(
        "SELECT * FROM serversubmissions WHERE id = $1;", sub_id
    )


async def edit_server(
    *,
    server_id,
    name=None,
    invite=None,
    categories=None,
    keywords=None,
    description=None
):
    if name is not None:
        await execute_query(
            "UPDATE servers SET name = $1 WHERE id = $2;", name, server_id
        )
    if invite is not None:
        await execute_query(
            "UPDATE servers SET invite = $1 WHERE id = $2;", invite, server_id
        )
    if categories is not None:
        await execute_query(
            "UPDATE servers SET categories = $1 WHERE id = $2", categories, server_id
        )
    if keywords is not None:
        await execute_query(
            "UPDATE servers SET keywords = $1 WHERE id = $2;", keywords, server_id
        )
    if description is not None:
        await execute_query(
            "UPDATE servers SET description = $1 WHERE id = $2;", description, server_id
        )


async def get_server(*, server_id):
    return (
        await execute_read_query(
            """
        SELECT * FROM servers
        WHERE id = $1;
    """,
            server_id,
        )
    )[0]
