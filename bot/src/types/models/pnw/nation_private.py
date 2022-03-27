from __future__ import annotations

import decimal
from typing import Optional, TypedDict

from ...resources import Resources

__all__ = ("NationPrivate",)


class NationPrivate(TypedDict):
    id: int
    update_tz: Optional[decimal.Decimal]
    spies: Optional[int]
    resources: Optional[Resources]
