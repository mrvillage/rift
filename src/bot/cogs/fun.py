from __future__ import annotations

from discord.ext import commands

from ...ref import Rift, RiftContext


class Fun(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.command(
        name="toot",
        brief="Toot tooooooot!",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def toot(self, ctx: RiftContext):
        await ctx.send("Toot tooooooot!")


def setup(bot: Rift):
    bot.add_cog(Fun(bot))
