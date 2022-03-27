from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Bankrec",)

if TYPE_CHECKING:
    import decimal
    from typing import ClassVar

    from pnwkit.data import Bankrec as PnWKitBankrec

    from ... import models
    from ...types.models.pnw.bankrec import Bankrec as BankrecData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Bankrec:
    TABLE: ClassVar[str] = "bankrecs"
    id: int
    date: datetime.datetime
    sender_id: int
    sender_type: enums.BankrecParticipantType = attrs.field(
        converter=enums.BankrecParticipantType
    )
    receiver_id: int
    receiver_type: enums.BankrecParticipantType = attrs.field(
        converter=enums.BankrecParticipantType
    )
    banker_id: int
    note: str
    resources: models.Resources
    tax_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: BankrecData) -> Bankrec:
        ...

    def to_dict(self) -> BankrecData:
        ...

    def update(self, data: Bankrec) -> Bankrec:
        ...

    @classmethod
    def from_data(cls, data: PnWKitBankrec) -> Bankrec:
        if TYPE_CHECKING:
            assert isinstance(data.money, decimal.Decimal)
            assert isinstance(data.coal, decimal.Decimal)
            assert isinstance(data.oil, decimal.Decimal)
            assert isinstance(data.uranium, decimal.Decimal)
            assert isinstance(data.iron, decimal.Decimal)
            assert isinstance(data.bauxite, decimal.Decimal)
            assert isinstance(data.lead, decimal.Decimal)
            assert isinstance(data.gasoline, decimal.Decimal)
            assert isinstance(data.munitions, decimal.Decimal)
            assert isinstance(data.steel, decimal.Decimal)
            assert isinstance(data.aluminum, decimal.Decimal)
            assert isinstance(data.food, decimal.Decimal)
        return cls(
            id=int(data.id),
            date=datetime.datetime.fromisoformat(data.date),
            sender_id=int(data.sid),
            # attrs will automatically convert the type
            sender_type=data.stype,  # type: ignore
            receiver_id=int(data.rid),
            receiver_type=data.rtype,  # type: ignore
            banker_id=int(data.pid),
            note=data.note,
            resources=models.Resources(
                money=data.money,
                coal=data.coal,
                oil=data.oil,
                uranium=data.uranium,
                iron=data.iron,
                bauxite=data.bauxite,
                lead=data.lead,
                gasoline=data.gasoline,
                munitions=data.munitions,
                steel=data.steel,
                aluminum=data.aluminum,
                food=data.food,
            ),
            tax_id=int(data.tax_id),
        )
