from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Account",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from .. import models


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Account:
    TABLE: ClassVar[str] = "accounts"
    id: int
    name: str
    owner_id: int
    alliance_id: int
    resources: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )
    war_chest: bool
    primary: bool
    deposit_code: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Account:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Account) -> Account:
        ...
