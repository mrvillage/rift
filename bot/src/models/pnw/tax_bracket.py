from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("TaxBracket",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from pnwkit.data import TaxBracket as PnWKitTaxBracket

    from ...types.models.pnw.tax_bracket import TaxBracket as TaxBracketData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TaxBracket:
    TABLE: ClassVar[str] = "tax_brackets"
    id: int
    alliance_id: int
    name: str
    date: datetime.datetime
    date_modified: datetime.datetime
    last_modifier_id: int
    tax_rate: int
    resource_tax_rate: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TaxBracketData) -> TaxBracket:
        ...

    def to_dict(self) -> TaxBracketData:
        ...

    def update(self, data: TaxBracket) -> TaxBracket:
        ...

    @classmethod
    def from_data(cls, data: PnWKitTaxBracket) -> TaxBracket:
        return cls(
            id=int(data.id),
            alliance_id=int(data.alliance_id),
            name=data.bracket_name,
            date=datetime.datetime.fromisoformat(data.date),
            date_modified=datetime.datetime.fromisoformat(data.date_modified),
            last_modifier_id=int(data.last_modifier_id),
            tax_rate=data.tax_rate,
            resource_tax_rate=data.resource_tax_rate,
        )
