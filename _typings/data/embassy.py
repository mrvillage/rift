from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("EmbassyData", "EmbassyConfigData")


class EmbassyData(TypedDict):
    id: int
    alliance: int
    config: int
    guild: int
    open: bool


class EmbassyConfigData(TypedDict):
    id: int
    category: Optional[int]
    guild: int
    start_message: str
