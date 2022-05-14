from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("Transaction",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar

    from .. import models


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Transaction:
    TABLE: ClassVar[str] = "transactions"
    id: int
    date: datetime.datetime
    status: enums.TransactionStatus = attrs.field(converter=enums.TransactionStatus)
    type: enums.TransactionType = attrs.field(converter=enums.TransactionType)
    creator_id: int
    to_id: int
    to_type: enums.AccountType = attrs.field(converter=enums.AccountType)
    from_id: int
    from_type: enums.AccountType = attrs.field(converter=enums.AccountType)
    resources: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )
    note: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Transaction:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Transaction) -> Transaction:
        ...
