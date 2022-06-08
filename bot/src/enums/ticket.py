from __future__ import annotations

import enum

__all__ = ("TicketCloseAction",)


class TicketCloseAction(enum.Enum):
    DELETE = 0
    ARCHIVE = 1
