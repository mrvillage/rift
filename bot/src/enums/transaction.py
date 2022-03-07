from __future__ import annotations

from enum import Enum

__all__ = ("TransactionType", "TransactionStatus")


class TransactionType(Enum):
    TRANSFER = 0
    DEPOSIT = 1
    WITHDRAW = 2
    GRANT = 3
    GRANT_WITHDRAW = 4
    GRANT_DEPOSIT = 5


class TransactionStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CANCELLED = 3
    FAILED = 4