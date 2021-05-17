import discord
from discord.ext import commands
from ... import funcs as rift


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if ctx.command.has_error_handler():
            return
        cog = ctx.cog
        if cog and commands.Cog._get_overridden_method(cog.cog_command_error) is not None:
            return
        await rift.handler(ctx, error)


def setup(bot):
    bot.add_cog(Errors(bot))
