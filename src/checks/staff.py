from discord.ext.commands import check


def is_staff():
    def predicate(ctx):
        return ctx.bot.is_owner(ctx.author) or ctx.author.id in ctx.bot.staff

    return check(predicate)
