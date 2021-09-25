from __future__ import annotations

from typing import TypedDict

__all__ = (
    "ForumData",
    "ForumPostData",
)


class ForumData(TypedDict):
    id: int
    link: str
    name: str


class ForumPostData(TypedDict):
    id: int
    link: str
    forum_id: int
