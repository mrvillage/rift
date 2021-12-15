from __future__ import annotations

import discord
from discord.ext import commands
from discord.utils import MISSING

from ...data.classes import Resources
from ...ref import Rift, RiftContext


class Grants(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="grant",
        brief="A group of commands related to grants.",
        type=commands.CommandType.chat_input,
    )
    async def grant(self, ctx: RiftContext):
        ...

    @grant.command(  # type: ignore
        name="send", brief="Send a grant.", type=commands.CommandType.chat_input
    )
    async def grant_send(
        self, ctx: RiftContext, resources: Resources, note: str = MISSING
    ):
        ...


def setup(bot: Rift):
    bot.add_cog(Grants(bot))
