__all__ = ("BaseError", "SearchError", "ConvertError")


class BaseError(Exception):
    ...


class SearchError(BaseError):
    ...


class ConvertError(BaseError):
    ...
