from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("TaxBracket",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar

    from pnwkit.data import TaxBracket as PnWKitTaxBracket


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TaxBracket:
    TABLE: ClassVar[str] = "tax_brackets"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    id: int
    alliance_id: int
    name: str
    date: datetime.datetime
    date_modified: datetime.datetime
    last_modifier_id: int
    tax_rate: int
    resource_tax_rate: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaxBracket:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: TaxBracket) -> TaxBracket:
        ...

    @classmethod
    def from_data(cls, data: PnWKitTaxBracket) -> TaxBracket:
        return cls(
            id=data.id,
            alliance_id=data.alliance_id,
            name=data.bracket_name,
            date=data.date,
            date_modified=data.date_modified,
            last_modifier_id=data.last_modifier_id,
            tax_rate=data.tax_rate,
            resource_tax_rate=data.resource_tax_rate,
        )
