from __future__ import annotations

from enum import Enum

__all__ = ("TransactionType", "TransactionStatus")


class TransactionType(Enum):
    TRANSFER = 0
    DEPOSIT = 1
    WITHDRAW = 2
    GRANT = 3


class TransactionStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CANCELLED = 3
