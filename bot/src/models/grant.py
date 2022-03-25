from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("Grant",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from .. import models
    from ..types.models.grant import Grant as GrantData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Grant:
    TABLE: ClassVar[str] = "grants"
    id: int
    date: datetime.datetime
    status: enums.GrantStatus = attrs.field(converter=enums.GrantStatus)
    recipient: int
    resources: models.Resources
    alliance_id: int
    note: str
    payoff_type: enums.GrantPayoffType = attrs.field(converter=enums.GrantPayoffType)
    deadline: datetime.datetime
    expiry: datetime.datetime
    paid: models.Resources
    payoff_code: str
    tax_bracket: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: GrantData) -> Grant:
        ...
