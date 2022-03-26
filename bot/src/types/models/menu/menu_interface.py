from __future__ import annotations

from typing import TypedDict

__all__ = ("MenuInterface",)


class MenuInterface(TypedDict):
    id: int
    menu_id: int
    message_id: int
    channel_id: int
