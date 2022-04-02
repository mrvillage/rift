from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Trade",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from pnwkit.data import Trade as PnWKitTrade

    from ...types.models.pnw.trade import Trade as TradeData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Trade:
    TABLE: ClassVar[str] = "trades"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("type", "action")
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

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TradeData) -> Trade:
        ...

    def to_dict(self) -> TradeData:
        ...

    def update(self, data: Trade) -> Trade:
        ...

    @classmethod
    def from_data(cls, data: PnWKitTrade) -> Trade:
        return cls(
            id=int(data.id),
            type=getattr(enums.TradeType, data.type),
            date=datetime.datetime.fromisoformat(data.date),
            sender_id=int(data.sid),
            receiver_id=int(data.rid),
            resource=getattr(enums.Resource, data.offer_resource.upper()),
            amount=data.offer_amount,
            action=getattr(enums.TradeAction, data.buy_or_sell.upper()),
            accepted=data.accepted,
            date_accepted=datetime.datetime.fromisoformat(data.date_accepted),
        )
