from .. import funcs as rift
from discord.ext.commands import UserConverter, UserNotFound
from ..errors import NationNotFoundError


async def search_nation_author(ctx, search):
    author = ctx.author if search is None else None
    search = str(ctx.author.id) if search is None else search
    try:
        nation = await rift.search_nation(ctx, search)
    except NationNotFoundError:
        if int(search) == ctx.author.id:
            await ctx.reply(ctx.author, f"No link found")
            return
        else:
            await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No nation found with argument `{search}`."))
            raise NationNotFoundError
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
