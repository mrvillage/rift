from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("TransactionData", "TransactionRequestData")


class TransactionData(TypedDict):
    id: int
    time: str
    status: int
    type: int
    creator: int
    to_: int
    from_: int
    resources: str
    note: Optional[str]
    to_type: int
    from_type: int


class TransactionRequestData(TypedDict):
    id: int
    transaction: int
    user_: int
    accept_custom_id: str
    reject_custom_id: str
    cancel_custom_id: str
