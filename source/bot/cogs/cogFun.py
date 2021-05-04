import discord
import asyncio
import json
from discord.ext import commands
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="toot")
    async def link(self, ctx):
        await ctx.send("Toot tooooooot!")


def setup(bot):
    bot.add_cog(Fun(bot))