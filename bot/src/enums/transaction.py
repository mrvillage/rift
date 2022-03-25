from __future__ import annotations

import enum

__all__ = ("AccountType", "TransactionStatus", "TransactionType")


class AccountType(enum.Enum):
    ACCOUNT = 0


class TransactionStatus(enum.Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CANCELLED = 3
    FAILED = 4


class TransactionType(enum.Enum):
    TRANSFER = 0
    DEPOSIT = 1
    WITHDRAW = 2
    GRANT = 3
    GRANT_WITHDRAW = 4
    GRANT_DEPOSIT = 5
