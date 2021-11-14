from __future__ import annotations

from typing import List, Optional

from ...cache import cache
from ...data.classes import Alliance, Credentials
from ..utils import get_alliance_position_id

__all__ = ("find_alliance_credentials",)


def find_alliance_credentials(
    alliance: Alliance, /, *permissions_required: str
) -> List[Credentials]:
    return [
        credentials
        for credentials in cache.credentials
        if credentials.nation is not None
        and credentials.nation.alliance is alliance
        and all(
            getattr(credentials.permissions, permission, False)
            for permission in permissions_required
        )
    ]


def find_highest_alliance_credentials(
    alliance: Alliance, /, *permissions_required: str
) -> Optional[Credentials]:
    credentials = find_alliance_credentials(alliance, *permissions_required)
    if credentials:
        return max(
            credentials,
            key=lambda c: get_alliance_position_id(c.nation.alliance_position),  # type: ignore
        )
