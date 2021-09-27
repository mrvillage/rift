from discord.ext.commands import check


def is_owner():
    async def predicate(ctx):
        return await ctx.bot.is_owner(ctx.author)

    return check(predicate)
