from discord.ext.commands import UserConverter, UserNotFound

from .. import funcs


async def search_nation_author(ctx, search):
    author = ctx.author if search is None else None
    search = str(ctx.author.id) if search is None else search
    nation = await funcs.search_nation(ctx, search)
    if author is None:
        try:
            author = await funcs.get_link_nation(nation.id)
            try:
                author = await UserConverter().convert(ctx, str(author))
            except UserNotFound:
                author = ctx.author if ctx.guild is None else ctx.guild
        except IndexError:
            author = ctx.author if ctx.guild is None else ctx.guild
    return author, nation


async def search_nation(ctx, search):
    search = str(ctx.author.id) if search is None else search
    return await funcs.search_nation(ctx, search)
