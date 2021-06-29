import json
from discord.ext.commands import InviteConverter, BadInviteArgument
from .. import cache
from ..errors import ServerNotFoundError
from .embeds import get_embed_author_member
from ..menus import EmbedPageSource, MenuPages
from ..data import get
from ..data.classes import Server

NEWLINE = "\n"


async def search_server(*args):
    args = [arg.lower() for arg in args]
    docs = [
        doc
        for doc in cache.servers.values()
        if any(arg in doc.search_args for arg in args)
    ]
    if len(docs) > 0:
        return docs
    else:
        raise ServerNotFoundError


search_servers = search_server


async def get_server_embeds(ctx, servers):
    invalid = []
    for server in servers:
        try:
            await InviteConverter().convert(ctx, server.invite)
        except BadInviteArgument:
            invalid.append(server)
    if len(servers) == 1:
        return (
            get_embed_author_member(
                ctx.author,
                description=f'[{servers[0].name} - {servers[0].id}]({servers[0].invite} "{servers[0].invite}")'
                + f"{f'{NEWLINE}{NEWLINE}{servers[0].description}' if servers[0].description is not None else ''}"
                + f"{f'{NEWLINE}INVALID LINK' if server in invalid else ''}",
                fields=[
                    {
                        "name": "Categories",
                        "value": ", ".join(servers[0].categories)
                        if servers[0].categories is not None
                        else "None",
                    },
                    {
                        "name": "Keywords",
                        "value": ", ".join(servers[0].keywords)
                        if servers[0].keywords is not None
                        else "None",
                    },
                ],
            ),
            invalid,
        )
    else:
        l = len(servers)
        embeds = [
            get_embed_author_member(
                ctx.author,
                title=server.name,
                description=f'[Server ID: {server.id}]({server.invite} "{server.invite}")'
                + f"{f'{NEWLINE}{NEWLINE}{server.description}' if server.description is not None else ''}"
                + f"{f'{NEWLINE}INVALID LINK' if server in invalid else ''}",
                fields=[
                    {
                        "name": "Categories",
                        "value": ", ".join(server.categories)
                        if server.categories is not None
                        else "None",
                    },
                    {
                        "name": "Keywords",
                        "value": ", ".join(server.keywords)
                        if server.keywords is not None
                        else "None",
                    },
                ],
                footer=f"Page {servers.index(server)+1}/{l}",
            )
            for server in servers
        ]
        embeds.insert(
            0,
            get_embed_author_member(
                ctx.author,
                title="Search Results",
                description="\n".join([str(doc.name) for doc in servers]),
                footer=f"{l} Pages",
            ),
        )
        return MenuPages(EmbedPageSource(embeds, per_page=1), timeout=30), invalid


async def submit_server(*, invite: str, status: bool = None, userid: int):
    await get.add_submit_server(invite=invite, status=status, userid=userid)


async def get_server_submissions(*, fil=None):
    if fil is None:
        return await get.get_server_submissions_pending()
    elif fil == "all":
        return await get.get_server_submissions()
    elif fil:
        return await get.get_server_submissions_approved()
    else:
        return await get.get_server_submissions_denied()


async def get_server_submission(*, sub_id):
    return await get.get_server_submission(sub_id=sub_id)


async def edit_server_submission(*, sub_id, status):
    await get.edit_server_submission(sub_id=sub_id, status=status)


async def add_server(
    *, name=None, invite=None, categories=None, keywords=None, description=None
):
    await get.add_server(
        name=name,
        invite=invite,
        categories=categories if categories is None else json.dumps(categories),
        keywords=keywords if keywords is None else json.dumps(keywords),
        description=description,
    )
    server_id = max(await get.get_server_ids())
    cache.servers[server_id] = Server(data=await get.get_server(server_id=server_id))
    return server_id


async def edit_server(
    *,
    server_id,
    name=None,
    invite=None,
    categories=None,
    keywords=None,
    description=None,
):
    await get.edit_server(
        server_id=server_id,
        name=name,
        invite=invite,
        categories=categories if categories is None else json.dumps(categories),
        keywords=keywords if keywords is None else json.dumps(keywords),
        description=description,
    )
    cache.servers[server_id] = Server(data=await get.get_server(server_id=server_id))
