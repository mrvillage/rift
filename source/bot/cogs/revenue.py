from typing import Union
from discord.ext import commands
from ... import funcs as rift
from ...data.classes import Alliance, Nation

class Revenue(commands.Cog):
    def __init__(self, bot: rift.Rift):
        self.bot = bot

    @commands.command(name="revenue")
    async def revenue(self, ctx, *, search: Union[Alliance, Nation]):
        pass


def setup(bot: rift.Rift):
    bot.add_cog(Revenue(bot))
