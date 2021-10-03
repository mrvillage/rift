from __future__ import annotations

from typing import TypedDict

__all__ = ("Field",)


class FieldOptional(TypedDict, total=False):
    inline: bool


class Field(FieldOptional):
    name: str
    value: str
