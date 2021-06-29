from .. import cache
from ..errors import DocumentNotFoundError
from .embeds import get_embed_author_member
from ..menus import EmbedPageSource, MenuPages
from ..data import get
from ..data.classes import Document
import json


async def search_document(*args):
    args = [arg.lower() for arg in args]
    docs = [
        doc
        for doc in cache.documents.values()
        if any(arg in doc.search_args for arg in args)
    ]
    if len(docs) > 0:
        return docs
    else:
        raise DocumentNotFoundError


search_documents = search_document


async def get_document_embeds(author, docs):
    if len(docs) == 1:
        return get_embed_author_member(
            author,
            description=f'[{docs[0].name} - {docs[0].id}]({docs[0].url} "{docs[0].url}")'
            + f"\n\n{docs[0].description.encode('utf-8').decode('unicode-escape') if docs[0].description is not None else ''}",
            fields=[
                {
                    "name": "Categories",
                    "value": ", ".join(docs[0].categories)
                    if docs[0].categories is not None
                    else "None",
                },
                {
                    "name": "Keywords",
                    "value": ", ".join(docs[0].keywords)
                    if docs[0].keywords is not None
                    else "None",
                },
            ],
        )
    else:
        l = len(docs)
        embeds = [
            get_embed_author_member(
                author,
                title=doc.name,
                description=f'[Document ID: {doc.id}]({doc.url} "{doc.url}")'
                + f"\n\n{doc.description.encode('utf-8').decode('unicode-escape') if doc.description is not None else ''}",
                fields=[
                    {
                        "name": "Categories",
                        "value": ", ".join(doc.categories)
                        if doc.categories is not None
                        else "None",
                    },
                    {
                        "name": "Keywords",
                        "value": ", ".join(doc.keywords)
                        if doc.keywords is not None
                        else "None",
                    },
                ],
                footer=f"Page {docs.index(doc)+1}/{l}",
            )
            for doc in docs
        ]
        embeds.insert(
            0,
            get_embed_author_member(
                author,
                title="Search Results",
                description="\n".join([str(doc.name) for doc in docs]),
                footer=f"{l} Pages",
            ),
        )
        return MenuPages(EmbedPageSource(embeds, per_page=1), timeout=30)


async def submit_document(*, url: str, status: bool = None, userid: int):
    await get.add_submit_document(url=url, status=status, userid=userid)


async def get_document_submissions(*, fil=None):
    if fil is None:
        return await get.get_document_submissions_pending()
    elif fil == "all":
        return await get.get_document_submissions()
    elif fil:
        return await get.get_document_submissions_approved()
    else:
        return await get.get_document_submissions_denied()


async def get_document_submission(*, sub_id):
    return await get.get_document_submission(sub_id=sub_id)


async def edit_document_submission(*, sub_id, status):
    await get.edit_document_submission(sub_id=sub_id, status=status)


async def add_document(
    *, name=None, url=None, categories=None, keywords=None, description=None
):
    await get.add_document(
        name=name,
        url=url,
        categories=categories if categories is None else json.dumps(categories),
        keywords=keywords if keywords is None else json.dumps(keywords),
        description=description,
    )
    doc_id = max(await get.get_document_ids())
    cache.documents[doc_id] = Document(data=await get.get_document(document_id=doc_id))
    return doc_id


async def edit_document(
    *,
    document_id,
    name=None,
    url=None,
    categories=None,
    keywords=None,
    description=None,
):
    await get.edit_document(
        document_id=document_id,
        name=name,
        url=url,
        categories=categories if categories is None else json.dumps(categories),
        keywords=keywords if keywords is None else json.dumps(keywords),
        description=description,
    )
    cache.documents[document_id] = Document(
        data=await get.get_document(document_id=document_id)
    )
