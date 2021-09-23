from __future__ import annotations

from typing import TYPE_CHECKING, List

import discord
from discord.ext import commands
from discord.utils import MISSING

from ...cache import cache
from ...errors import SubscriptionNotFoundError
from ...ref import bot
from ..db import execute_query

__all__ = ("Subscription",)

if TYPE_CHECKING:
    from typings import EventCategoryLiteral, EventTypeLiteral, SubscriptionData


class Subscription:
    __slots__ = (
        "id",
        "token",
        "guild_id",
        "channel_id",
        "category",
        "type",
        "sub_types",
        "arguments",
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
        self.arguments: List[int] = data["arguments"]

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str, /) -> Subscription:
        try:
            return await cls.fetch(int(argument))
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
            self._webhook = discord.Webhook.from_state(
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
        arguments: List[int] = [],
        /,
    ) -> Subscription:
        webhook = await channel.create_webhook(
            name=f"{category}_{type}",
            avatar=bot.bytes_avatar,
            reason=f"Subscribed to event {category}_{type}",
        )
        data: SubscriptionData = {
            "id": webhook.id,
            "token": webhook.token,
            "guild_id": channel.guild.id,
            "channel_id": channel.id,
            "category": category,
            "type": type,
            "sub_types": sub_types,
            "arguments": arguments,
        }
        subscription = cls(data)
        cache._subscriptions[subscription.id] = subscription
        await subscription.save()
        return subscription

    async def delete(self) -> None:
        try:
            await self.webhook.delete(reason="Subscription deleted")
        except discord.NotFound as e:
            if e.code != 10015:
                raise
        cache._subscriptions.pop(self.id)
        await execute_query(
            "DELETE FROM subscriptions WHERE id = $1;",
            self.id,
        )

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO subscriptions (id, token, guild_id, channel_id, category, type, sub_types, arguments) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);",
            self.id,
            self.token,
            self.guild_id,
            self.channel_id,
            self.category,
            self.type,
            self.sub_types,
            self.arguments,
        )

    async def send(self, embed: discord.Embed, send_view: bool = True, /) -> None:
        from ...views import EventExtraInformationView

        try:
            view: EventExtraInformationView = (
                EventExtraInformationView() if send_view else MISSING
            )
            await self.webhook.send(embed=embed, view=view)
        except discord.NotFound as e:
            if e.code == 10015:
                await self.delete()
            else:
                raise
