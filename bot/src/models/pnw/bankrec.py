from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs

from ... import enums, models, utils

__all__ = ("Bankrec",)

if TYPE_CHECKING:
    import decimal
    from typing import Any, ClassVar

    from pnwkit.data import Bankrec as PnWKitBankrec


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Bankrec:
    TABLE: ClassVar[str] = "bankrecs"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("sender_type", "receiver_type")
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
    resources: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )
    tax_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Bankrec:
        ...

    def to_dict(self) -> dict[str, Any]:
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
            id=data.id,
            date=data.date,
            sender_id=data.sender_id,
            # attrs will automatically convert the type
            sender_type=data.sender_type,  # type: ignore
            receiver_id=data.receiver_id,
            receiver_type=data.receiver_type,  # type: ignore
            banker_id=data.banker_id,
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
            tax_id=data.tax_id,
        )
