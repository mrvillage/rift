from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Bankrec",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from ... import models
    from ...types.models.pnw.bankrec import Bankrec as BankrecData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Bankrec:
    TABLE: ClassVar[str] = "bankrecs"
    id: int
    date: datetime.datetime
    sender_id: int
    sender_type: enums.ModelType = attrs.field(converter=enums.ModelType)
    receiver_id: int
    receiver_type: enums.ModelType = attrs.field(converter=enums.ModelType)
    banker_id: int
    note: str
    resources: models.Resources
    tax_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: BankrecData) -> Bankrec:
        ...
