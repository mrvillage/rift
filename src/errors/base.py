from __future__ import annotations

__all__ = ("BaseError", "SearchError", "ConvertError")


class BaseError(Exception):
    ...


class SearchError(BaseError):
    ...


class ConvertError(BaseError):
    ...
