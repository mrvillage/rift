from __future__ import annotations

from typing import TYPE_CHECKING

from ...cache import cache
from ...errors import ForumNotFoundError
from ...funcs.utils import convert_int
from ...ref import RiftContext
from ..db import execute_query

__all__ = (
    "Forum",
    "ForumPost",
)

if TYPE_CHECKING:
    from _typings import ForumData, ForumPostData


class Forum:
    __slots__ = ("id", "link", "name")

    def __init__(self, data: ForumData):
        self.id: int = data["id"]
        self.link: str = data["link"]
        self.name: str = data["name"]

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Forum:
        try:
            forum = cache.get_forum(convert_int(argument))
            if forum:
                return forum
        except ValueError:
            pass
        try:
            return next(
                i
                for i in cache.forums
                if i.name.lower() == argument.lower().replace("_", " ").strip(" _")
            )
        except StopIteration:
            raise ForumNotFoundError(argument)


class ForumPost:
    __slots__ = ("id", "link", "forum_id")

    def __init__(self, data: ForumPostData):
        self.id: int = data["id"]
        self.link: str = data["link"]
        self.forum_id: int = data["forum"]

    @property
    def forum(self) -> Forum:
        return cache.get_forum(self.forum_id)  # type: ignore

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO forum_posts (id, link, forum) VALUES ($1, $2, $3);",
            self.id,
            self.link,
            self.forum_id,
        )
