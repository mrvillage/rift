from discord.ext import commands


def has_manage_permissions():
    async def predicate(ctx: commands.Context):
        perms = ctx.author.guild_permissions
        if (
            perms.manage_guild
            or perms.administrator
            or ctx.guild.owner_id == ctx.author.id
        ):
            return True
        raise commands.MissingPermissions(["manage"])

    return commands.check(predicate)
