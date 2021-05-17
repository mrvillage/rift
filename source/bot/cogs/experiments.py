import discord
from discord.ext import commands

from ...data.query import get_mmr


class Experiments(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mmr")
    async def mmr(self, ctx):
        print(await get_mmr(mmr_id=1))


def setup(bot):
    bot.add_cog(Experiments(bot))