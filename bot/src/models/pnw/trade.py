from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Trade",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from ...types.models.pnw.trade import Trade as TradeData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Trade:
    TABLE: ClassVar[str] = "trades"
    id: int
    type: enums.TradeType = attrs.field(converter=enums.TradeType)
    date: datetime.datetime
    sender_id: int
    receiver_id: int
    resource: enums.Resource
    amount: int
    action: enums.TradeAction
    accepted: bool
    date_accepted: datetime.datetime

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TradeData) -> Trade:
        ...
