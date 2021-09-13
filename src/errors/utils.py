from .base import ConvertError

__all__ = ("BoolError", "LinkError")


class BoolError(ConvertError):
    pass


class LinkError(ConvertError):
    pass
