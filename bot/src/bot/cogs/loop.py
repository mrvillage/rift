from __future__ import annotations

import datetime

import discord
from discord.ext import commands, tasks

from ...ref import Rift


class Loop(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.pnw_session_refresh.start()

    @tasks.loop(minutes=5)
    async def pnw_session_refresh(self):
        await self.bot.update_pnw_session()

    @pnw_session_refresh.before_loop
    async def pnw_session_refresh_wait(self):
        now = datetime.datetime.utcnow()
        wait = now.replace(minute=5, second=0)
        while wait < now:
            wait += datetime.timedelta(minutes=10)
        # wait = now
        await discord.utils.sleep_until(wait)


def setup(bot: Rift):
    bot.add_cog(Loop(bot))
