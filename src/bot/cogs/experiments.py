from typing import Optional
from discord.ext import commands

from ...data.query import get_mmr


class Experiments(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mmr")
    async def mmr(self, ctx):
        print(await get_mmr(mmr_id=1))

    class Flags(
        commands.FlagConverter, case_insensitive=True, delimiter="=", prefix="-"
    ):
        hi: Optional[str] = commands.flag(name="hi", default=lambda ctx: [])
        hello: Optional[str] = commands.flag(name="hello", default=lambda ctx: [])

    @commands.command(name="flags")
    async def flags(self, ctx, flags: Flags, *, kwarg=None):
        await ctx.send(str(kwarg))
        await ctx.send(str(flags))


def setup(bot):
    bot.add_cog(Experiments(bot))
