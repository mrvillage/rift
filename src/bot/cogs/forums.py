from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import aiohttp
import discord
import feedparser
from discord.ext import commands, tasks

from ...data.classes import ForumPost
from ...data.db import execute_read_query
from ...ref import Rift


class Forums(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.check_alliance_affairs.start()

    @tasks.loop(minutes=1)
    async def check_alliance_affairs(self):
        async with aiohttp.request(
            "GET",
            "https://forum.politicsandwar.com/index.php?/forum/42-alliance-affairs.xml",
        ) as r:
            m = (
                await execute_read_query(
                    "SELECT MAX(id) FROM forum_posts WHERE forum_id = 42;"
                )
            )[0]["max"]
            feed = feedparser.parse(await r.text())
            for entry in feed.entries:
                try:
                    g = int(entry.guid)  # type: ignore
                except (ValueError, AttributeError):
                    continue
                if g > m:
                    if TYPE_CHECKING:
                        assert isinstance(entry.guid, int) and isinstance(
                            entry.link, str
                        )
                    post = ForumPost(
                        {"id": int(entry.guid), "link": entry.link, "forum_id": 42}
                    )
                    await post.save()
                    self.bot.dispatch("forum_post_create", post, entry.title)

    @check_alliance_affairs.before_loop
    async def before_check_alliance_affairs(self):
        await self.bot.wait_until_ready()


def setup(bot: Rift):
    bot.add_cog(Forums(bot))
