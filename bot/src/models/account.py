from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Account",)

if TYPE_CHECKING:
    from typing import ClassVar

    from .. import models
    from ..types.models.account import Account as AccountData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Account:
    TABLE: ClassVar[str] = "accounts"
    id: int
    name: str
    owner_id: int
    alliance_id: int
    resources: models.Resources
    war_chest: bool
    primary: bool
    deposit_code: str

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AccountData) -> Account:
        ...

    def to_dict(self) -> AccountData:
        ...
