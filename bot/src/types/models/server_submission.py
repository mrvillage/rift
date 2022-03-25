from __future__ import annotations

from typing import TypedDict

__all__ = ("ServerSubmission",)


class ServerSubmission(TypedDict):
    id: int
    name: str
    invite: str
    description: str
    tags: list[str]
