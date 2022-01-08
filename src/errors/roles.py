from __future__ import annotations

from .base import BaseError

__all__ = ("NoRolesError",)


class RolesError(BaseError):
    ...


class NoRolesError(RolesError):
    ...
