import discord
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not ctx.command.has_error_handler():
            await rift.handler(ctx, error)


def setup(bot):
    bot.add_cog(Errors(bot))
