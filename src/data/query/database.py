from ..db import execute_read_query


async def get_document(*, document_id):
    return (
        await execute_read_query(
            """
        SELECT * FROM documents
        WHERE id = $1;
    """,
            document_id,
        )
    )[0]


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


async def get_documents():
    return await execute_read_query(
        """
        SELECT * FROM documents;
    """
    )


async def get_servers():
    return await execute_read_query(
        """
        SELECT * FROM servers;
    """
    )
