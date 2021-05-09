from .. import funcs as rift
from ..errors import AllianceNotFoundError


async def search_alliance(ctx, search):
    search = str(ctx.author.id) if search is None else search
    try:
        alliance = await rift.search_alliance(ctx, search)
    except AllianceNotFoundError:
        await ctx.reply(embed=rift.get_embed_author_member(ctx.author, f"No alliance found with argument `{search}`."))
        raise AllianceNotFoundError
    return alliance
