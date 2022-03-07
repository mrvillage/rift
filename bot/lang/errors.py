from __future__ import annotations

__all__ = (
    "LangError",
    "InvalidAttributeError",
    "InvalidSyntaxError",
    "NotCallableError",
)


class LangError(Exception):
    ...


class InvalidAttributeError(LangError):
    ...


class InvalidSyntaxError(LangError):
    ...


class NotCallableError(LangError):
    ...
