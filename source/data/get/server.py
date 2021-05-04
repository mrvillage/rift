from ..db import execute_query, execute_read_query
from . import query


async def add_submit_document(*, url: str, status: bool, userid: int):
    await execute_query("INSERT INTO documentsubmissions (url, status, userid) VALUES ($1, $2, $3);", url, status, userid)


async def get_document_submissions():
    return await execute_read_query("SELECT * FROM documentsubmissions;")


async def get_document_submissions_pending():
    return await execute_read_query("SELECT * FROM documentsubmissions WHERE status is null;")


async def get_document_submissions_approved():
    return await execute_read_query("SELECT * FROM documentsubmissions WHERE status = true;")


async def get_document_submissions_denied():
    return await execute_read_query("SELECT * FROM documentsubmissions WHERE status = false;")


async def add_document(*, name=None, url=None, categories=None, keywords=None, description=None):
    await execute_query("INSERT INTO documents (name, url, categories, keywords, description) VALUES ($1, $2, $3, $4, $5);", name, url, categories, keywords, description)


async def edit_document_submission(*, sub_id, status):
    await execute_query("UPDATE documentsubmissions SET status = $1 WHERE id = $2;", status, sub_id)


async def get_document_ids():
    return [i[0] for i in await execute_read_query("SELECT id FROM documents;")]


async def get_document_submission(*, sub_id):
    return await execute_read_query("SELECT * FROM documentsubmissions WHERE id = $1;", sub_id)


async def edit_document(*, document_id, name=None, url=None, categories=None, keywords=None, description=None):
    if name is not None:
        await execute_query("UPDATE documents SET name = $1 WHERE id = $2;", name, document_id)
    if url is not None:
        await execute_query("UPDATE documents SET url = $1 WHERE id = $2;", url, document_id)
    if categories is not None:
        await execute_query("UPDATE documents SET categories = $1 WHERE id = $2", categories, document_id)
    if keywords is not None:
        await execute_query("UPDATE documents SET keywords = $1 WHERE id = $2;", keywords, document_id)
    if description is not None:
        await execute_query("UPDATE documents SET description = $1 WHERE id = $2;", description, document_id)


async def get_server(*, server_id):
    return await query.get_server(server_id=server_id)
