from __future__ import annotations

import enum

__all__ = ("MentionOwnerType",)


class MentionOwnerType(enum.Enum):
    BOT = 0
    USER = 1
