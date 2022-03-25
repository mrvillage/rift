from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AlliancePrivate",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ... import models
    from ...types.models.pnw.alliance_private import (
        AlliancePrivate as AlliancePrivateData,
    )


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AlliancePrivate:
    TABLE: ClassVar[str] = "alliances_private"
    id: int
    resources: models.Resources

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AlliancePrivateData) -> AlliancePrivate:
        ...
