from discord.ext.commands import UserConverter, UserNotFound

from .. import funcs as rift


async def search_nation_author(ctx, search):
    author = ctx.author if search is None else None
    search = str(ctx.author.id) if search is None else search
    nation = await rift.search_nation(ctx, search)
    if author is None:
        try:
            author = await rift.get_link_nation(nation.id)
            try:
                author = await UserConverter().convert(ctx, str(author[0]))
            except UserNotFound:
                author = ctx.guild
        except IndexError:
            author = ctx.guild
    return author, nation


async def search_nation(ctx, search):
    author = ctx.author if search is None else None
    search = str(ctx.author.id) if search is None else search
    return await rift.search_nation(ctx, search)
