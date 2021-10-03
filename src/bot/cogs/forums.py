from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp
import feedparser
from discord.ext import commands, tasks
from feedparser.util import FeedParserDict

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
            m: int = (
                await execute_read_query(
                    "SELECT MAX(id) FROM forum_posts WHERE forum_id = 42;"
                )
            )[0]["max"]
            feed: FeedParserDict = feedparser.parse(await r.text())  # type: ignore
            for entry in feed["entries"]:  # type: ignore
                entry: FeedParserDict
                try:
                    g = int(entry.guid)  # type: ignore
                except (ValueError, AttributeError):
                    continue
                if g > m:
                    if TYPE_CHECKING:
                        assert isinstance(entry["guid"], int) and isinstance(
                            entry["link"], str
                        )
                    post = ForumPost(
                        {
                            "id": int(entry["guid"]),  # type: ignore
                            "link": entry["link"],  # type: ignore
                            "forum_id": 42,
                        }
                    )
                    await post.save()
                    self.bot.dispatch("forum_post_create", post, entry["title"])

    @check_alliance_affairs.before_loop
    async def before_check_alliance_affairs(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=1)
    async def check_orbis_central(self):
        async with aiohttp.request(
            "GET",
            "https://forum.politicsandwar.com/index.php?/forum/40-orbis-central.xml",
        ) as r:
            m: int = (
                await execute_read_query(
                    "SELECT MAX(id) FROM forum_posts WHERE forum_id = 40;"
                )
            )[0]["max"]
            feed: FeedParserDict = feedparser.parse(await r.text())  # type: ignore
            for entry in feed["entries"]:  # type: ignore
                entry: FeedParserDict
                try:
                    g = int(entry.guid)  # type: ignore
                except (ValueError, AttributeError):
                    continue
                if g > m:
                    if TYPE_CHECKING:
                        assert isinstance(entry["guid"], int) and isinstance(
                            entry["link"], str
                        )
                    post = ForumPost(
                        {
                            "id": int(entry["guid"]),  # type: ignore
                            "link": entry["link"],  # type: ignore
                            "forum_id": 40,
                        }
                    )
                    await post.save()
                    self.bot.dispatch("forum_post_create", post, entry["title"])

    @check_orbis_central.before_loop
    async def before_check_orbis_central(self):
        await self.bot.wait_until_ready()


def setup(bot: Rift):
    bot.add_cog(Forums(bot))
