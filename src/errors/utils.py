from __future__ import annotations

from .base import ConvertError

__all__ = ("BoolError", "LinkError")


class BoolError(ConvertError):
    ...


class LinkError(ConvertError):
    ...
