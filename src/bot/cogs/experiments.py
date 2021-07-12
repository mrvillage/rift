from src.flags.base import BooleanFlagConverter
from typing import Optional
from discord.ext import commands
from discord.ext.commands.flags import FlagConverter

from ...data.query import get_mmr


class Flags(
    BooleanFlagConverter,
    case_insensitive=True,
    delimiter="=",
    prefix="-",
):
    hi: Optional[str]
    hello: Optional[str]


class Experiments(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mmr")
    async def mmr(self, ctx):
        print(await get_mmr(mmr_id=1))

    @commands.command(name="flags")
    async def flags(self, ctx, *, flags: Flags):
        # flags = Flags.parse_flags(flags)
        await ctx.send(str(flags))


def setup(bot):
    bot.add_cog(Experiments(bot))
