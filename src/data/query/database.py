from ..db import execute_read_query


async def query_document(*, document_id):
    return (
        await execute_read_query(
            """
        SELECT * FROM documents
        WHERE id = $1;
    """,
            document_id,
        )
    )[0]


async def query_server(*, server_id):
    return (
        await execute_read_query(
            """
        SELECT * FROM servers
        WHERE id = $1;
    """,
            server_id,
        )
    )[0]


async def query_documents():
    return await execute_read_query(
        """
        SELECT * FROM documents;
    """
    )


async def query_servers():
    return await execute_read_query(
        """
        SELECT * FROM servers;
    """
    )
