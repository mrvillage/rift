from .. import funcs as rift


async def search_alliance(ctx, search):
    search = str(ctx.author.id) if search is None else search
    return await rift.search_alliance(ctx, search)
