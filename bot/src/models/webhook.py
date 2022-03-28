from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Webhook",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.webhook import Webhook as WebhookData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Webhook:
    TABLE: ClassVar[str] = "webhooks"
    id: int
    channel_id: int
    guild_id: int
    token: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: WebhookData) -> Webhook:
        ...

    def to_dict(self) -> WebhookData:
        ...

    def update(self, data: Webhook) -> Webhook:
        ...
