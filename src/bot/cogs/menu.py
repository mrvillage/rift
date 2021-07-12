import discord
from discord.ext import commands
from ...ref import Rift


class Menu(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="menu", aliases=["role-menu", "rolemenu", "reaction-menu", "reactionmenu"]
    )
    async def menu(self, ctx: commands.Context):
        ...


def setup(bot: Rift):
    bot.add_cog(Menu(bot))
