from __future__ import annotations

import uuid
from typing import Optional, TypedDict

__all__ = ("User",)


class User(TypedDict):
    user_id: int
    nation_id: Optional[int]
    uuid: uuid.UUID
