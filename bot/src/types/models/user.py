from __future__ import annotations

import uuid
from typing import TypedDict

__all__ = ("User",)


class User(TypedDict):
    user_id: int
    nation_id: int
    uuid: uuid.UUID
