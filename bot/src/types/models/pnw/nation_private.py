from __future__ import annotations

import decimal
from typing import TypedDict

from ...resources import Resources

__all__ = ("NationPrivate",)


class NationPrivate(TypedDict):
    id: int
    update_tz: decimal.Decimal
    spies: int
    resources: Resources
