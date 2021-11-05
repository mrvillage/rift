from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type

import discord
from discord.utils import MISSING

from ...cache import cache
from ...data.classes import Condition
from ...errors import SubscriptionNotFoundError
from ...funcs.utils import convert_int
from ...ref import RiftContext, bot
from ..db import execute_query

__all__ = ("Subscription",)

if TYPE_CHECKING:
    from _typings import EventCategoryLiteral, EventTypeLiteral, SubscriptionData


class Subscription:
    __slots__ = (
        "id",
        "token",
        "guild_id",
        "channel_id",
        "category",
        "type",
        "sub_types",
        "condition",
        "_webhook",
    )

    def __init__(self, data: SubscriptionData) -> None:
        self.id: int = data["id"]
        self.token: str = data["token"]
        self.guild_id: int = data["guild_id"]
        self.channel_id: int = data["channel_id"]
        self.category: EventCategoryLiteral = data["category"]
        self.type: EventTypeLiteral = data["type"]
        self.sub_types: List[str] = data["sub_types"]
        self.condition: Optional[Condition] = (
            Condition.parse(data["condition"]) if data["condition"] else None
        )

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str, /) -> Subscription:
        try:
            subscription = await cls.fetch(convert_int(argument))
            if TYPE_CHECKING:
                assert isinstance(ctx.guild, discord.Guild)
            if subscription.guild_id != ctx.guild.id:
                raise SubscriptionNotFoundError(argument)
            return subscription
        except ValueError:
            raise SubscriptionNotFoundError(argument)

    @classmethod
    async def fetch(cls, id: int, /) -> Subscription:
        subscription = cache.get_subscription(id)
        if subscription is not None:
            return subscription
        raise SubscriptionNotFoundError(id)

    @property
    def webhook(self) -> discord.Webhook:
        try:
            return self._webhook
        except AttributeError:
            data = {
                "id": self.id,
                "token": self.token,
                "type": 3,
                "channel_id": self.channel_id,
                "guild_id": self.guild_id,
                "name": f"{self.category}_{self.type}",
            }
            self._webhook = discord.Webhook.from_state(  # type: ignore
                data, state=bot._connection  # type: ignore
            )
            return self._webhook

    @classmethod
    async def subscribe(
        cls,
        channel: discord.TextChannel,
        category: EventCategoryLiteral,
        type: EventTypeLiteral,
        sub_types: List[str] = [],
        /,
        condition: Condition = MISSING,
    ) -> Subscription:
        target = channel.parent if isinstance(channel, discord.Thread) else channel
        if TYPE_CHECKING:
            assert target is not None
        webhook = await target.create_webhook(
            name=f"{category}_{type}",
            avatar=bot.bytes_avatar,
            reason=f"Subscribed to event {category}_{type}",
        )
        data: SubscriptionData = {
            "id": webhook.id,
            "token": webhook.token,  # type: ignore
            "guild_id": channel.guild.id,
            "channel_id": channel.id,
            "category": category,
            "type": type,
            "sub_types": sub_types,
            "condition": str(condition) or None,
        }
        subscription = cls(data)
        cache.add_subscription(subscription)
        await subscription.save()
        return subscription

    async def delete(self) -> None:
        try:
            await self.webhook.delete(reason="Subscription deleted")
        except discord.NotFound as e:
            if e.code != 10015:
                raise
        cache.remove_subscription(self)
        await execute_query(
            "DELETE FROM subscriptions WHERE id = $1;",
            self.id,
        )

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO subscriptions (id, token, guild_id, channel_id, category, type, sub_types, condition) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);",
            self.id,
            self.token,
            self.guild_id,
            self.channel_id,
            self.category,
            self.type,
            self.sub_types,
            self.condition and str(self.condition),
        )

    async def send(
        self,
        embed: discord.Embed,
        send_view: bool = True,
        view: Type[discord.ui.View] = MISSING,
        /,
    ) -> None:
        from ...views import EventExtraInformationView

        view = view or EventExtraInformationView
        try:
            v: discord.ui.View = view() if send_view else MISSING
            await self.webhook.send(embed=embed, view=v)
        except discord.NotFound as e:
            if e.code == 10015:
                await self.delete()
            else:
                raise
