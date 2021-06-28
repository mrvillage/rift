import aiohttp
from discord.ext import commands
from ... import funcs as rift


class Events(commands.Cog):
    def __init__(self, bot: rift.Rift):
        self.bot = bot


def setup(bot: rift.Rift):
    bot.add_cog(Events(bot))
