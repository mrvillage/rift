from .base import SearchError


class MenuNotFoundError(SearchError):
    pass


class MenuItemNotFoundError(SearchError):
    pass
