from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("NationPrivate",)

if TYPE_CHECKING:
    import decimal
    from typing import ClassVar

    from ... import models
    from ...types.models.pnw.nation_private import NationPrivate as NationPrivateData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class NationPrivate:
    TABLE: ClassVar[str] = "nations_private"
    id: int
    update_tz: decimal.Decimal
    spies: int
    resources: models.Resources

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: NationPrivateData) -> NationPrivate:
        ...
