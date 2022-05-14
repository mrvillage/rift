from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("InactiveAlert",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InactiveAlert:
    TABLE: ClassVar[str] = "inactive_alerts"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("nation_id",)
    nation_id: int
    last_alert: datetime.datetime

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InactiveAlert:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: InactiveAlert) -> InactiveAlert:
        ...

    @property
    def key(self) -> int:
        return self.nation_id
