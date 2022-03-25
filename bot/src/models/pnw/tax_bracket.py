from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("TaxBracket",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

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
