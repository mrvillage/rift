from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING

import aiohttp
import discord
import feedparser
from discord.ext import commands, tasks
from feedparser.util import FeedParserDict

from ... import funcs
from ...data.classes import ForumPost
from ...data.db import execute_read_query
from ...ref import Rift


class Forums(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.check_alliance_affairs.start()
        self.check_orbis_central.start()

    @tasks.loop(minutes=1)
    async def check_alliance_affairs(self):
        try:
            await asyncio.wait_for(self._check_alliance_affairs(), timeout=600)
        except asyncio.TimeoutError:
            await self.send_loop_error("check_alliance_affairs")
        except Exception:
            pass

    async def _check_alliance_affairs(self):
        async with aiohttp.request(
            "GET",
            "https://forum.politicsandwar.com/index.php?/forum/42-alliance-affairs.xml",
        ) as r:
            m: int = (
                await execute_read_query(
                    "SELECT MAX(id) FROM forum_posts WHERE forum = 42;"
                )
            )[0]["max"]
            feed: FeedParserDict = feedparser.parse(await r.text())  # type: ignore
            for entry in feed["entries"]:  # type: ignore
                entry: FeedParserDict
                try:
                    g = int(entry["guid"])  # type: ignore
                except (ValueError, IndexError):
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
                            "forum": 42,
                        }
                    )
                    await post.save()
                    self.bot.dispatch("forum_post_create", post, entry["title"])

    @check_alliance_affairs.before_loop
    async def before_check_alliance_affairs(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=1)
    async def check_orbis_central(self):
        try:
            await asyncio.wait_for(self._check_orbis_central(), timeout=600)
        except asyncio.TimeoutError:
            await self.send_loop_error("check_orbis_central")
        except Exception:
            pass

    async def _check_orbis_central(self):
        async with aiohttp.request(
            "GET",
            "https://forum.politicsandwar.com/index.php?/forum/40-orbis-central.xml",
        ) as r:
            m: int = (
                await execute_read_query(
                    "SELECT MAX(id) FROM forum_posts WHERE forum = 40;"
                )
            )[0]["max"]
            feed: FeedParserDict = feedparser.parse(await r.text())  # type: ignore
            for entry in feed["entries"]:  # type: ignore
                entry: FeedParserDict
                try:
                    g = int(entry["guid"])  # type: ignore
                except (ValueError, IndexError):
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
                            "forum": 40,
                        }
                    )
                    await post.save()
                    self.bot.dispatch("forum_post_create", post, entry["title"])

    @check_orbis_central.before_loop
    async def before_check_orbis_central(self):
        await self.bot.wait_until_ready()

    async def send_loop_error(self, name: str):
        print(
            f"Loop {name} timed out",
            file=sys.stderr,
            flush=True,
        )
        sys.stderr.flush()
        channel = self.bot.get_channel(919428590167277609)
        if channel is not None:
            if TYPE_CHECKING:
                assert isinstance(channel, discord.TextChannel)
            try:
                await channel.send(
                    embed=funcs.get_embed_author_member(
                        self.bot.get_user(self.bot.user.id),  # type: ignore
                        f"Loop {name} timed out!",
                        color=discord.Color.red(),
                    )
                )
            except discord.HTTPException:
                print(
                    "Failed to send error message to errors channel.",
                    file=sys.stderr,
                    flush=True,
                )


def setup(bot: Rift):
    bot.add_cog(Forums(bot))
