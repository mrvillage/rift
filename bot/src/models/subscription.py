from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Subscription",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.subscription import Subscription as SubscriptionData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Subscription:
    TABLE: ClassVar[str] = "subscriptions"
    id: int
    guild_id: int
    channel_id: int
    owner_id: int
    event: str
    sub_types: list[str]
    condition: str
    mentions: list[int]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: SubscriptionData) -> Subscription:
        ...
