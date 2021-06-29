from discord.ext.commands import check


def is_owner():
    def predicate(ctx):
        return ctx.bot.is_owner(ctx.author)

    return check(predicate)
