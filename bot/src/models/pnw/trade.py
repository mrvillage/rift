from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Trade",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar

    from pnwkit.data import Trade as PnWKitTrade


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Trade:
    TABLE: ClassVar[str] = "trades"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("type", "resource", "action")
    id: int
    type: enums.TradeType = attrs.field(converter=enums.TradeType)
    date: datetime.datetime
    sender_id: int
    receiver_id: int
    resource: enums.Resource
    amount: int
    action: enums.TradeAction
    price: int
    accepted: bool
    date_accepted: datetime.datetime
    original_trade_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Trade:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Trade) -> Trade:
        ...

    @classmethod
    def from_data(cls, data: PnWKitTrade) -> Trade:
        return cls(
            id=data.id,
            type=getattr(enums.TradeType, data.type.name),
            date=data.date,
            sender_id=data.sender_id,
            receiver_id=data.receiver_id,
            resource=getattr(enums.Resource, data.offer_resource.upper()),
            amount=data.offer_amount,
            action=getattr(enums.TradeAction, data.buy_or_sell.upper()),
            price=data.price,
            accepted=bool(data.accepted),
            date_accepted=data.date_accepted,
            original_trade_id=data.original_trade_id,
        )
