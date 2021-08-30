from .. import funcs


async def search_alliance(ctx, search):
    search = str(ctx.author.id) if search is None else search
    return await funcs.search_alliance(ctx, search)
