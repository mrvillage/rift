from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("CityAutoRole",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    
        CityAutoRole as CityAutoRoleData,
    )


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class CityAutoRole:
    TABLE: ClassVar[str] = "city_auto_roles"
    id: int
    role_id: int
    guild_id: int
    min_city: int
    max_city: int
    members_only: bool
    condition: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CityAutoRole:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: CityAutoRole) -> CityAutoRole:
        ...
