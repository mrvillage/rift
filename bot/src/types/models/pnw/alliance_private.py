from __future__ import annotations

from typing import TypedDict

from ...resources import Resources

__all__ = ("AlliancePrivate",)


class AlliancePrivate(TypedDict):
    id: int
    resources: Resources
