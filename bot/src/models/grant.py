from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("Grant",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar

    from .. import models


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Grant:
    TABLE: ClassVar[str] = "grants"
    id: int
    date: datetime.datetime
    status: enums.GrantStatus = attrs.field(converter=enums.GrantStatus)
    recipient: int
    resources: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )
    alliance_id: int
    note: str
    payoff_type: enums.GrantPayoffType = attrs.field(converter=enums.GrantPayoffType)
    deadline: datetime.datetime
    expiry: datetime.datetime
    paid: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )
    payoff_code: str
    tax_bracket: int

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Grant:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Grant) -> Grant:
        ...
