from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from src.ref import RiftContext

from ...cache import cache
from ...errors import TicketConfigNotFoundError, TicketNotFoundError
from ...funcs.utils import convert_int
from ..db import execute_query, execute_read_query

__all__ = ("Ticket", "TicketConfig")

if TYPE_CHECKING:
    from _typings import TicketConfigData, TicketData


class Ticket:
    id: int
    ticket_number: int
    config_id: int
    guild_id: int
    user_id: int
    open: bool

    __slots__ = (
        "id",
        "ticket_number",
        "config_id",
        "guild_id",
        "user_id",
        "open",
    )

    def __init__(self, data: TicketData) -> None:
        self.id = data["id"]
        self.ticket_number = data["ticket_number"]
        self.config_id = data["config"]
        self.guild_id = data["guild"]
        self.user_id = data["user_"]
        self.open = data["open"]

    @classmethod
    async def fetch(cls, ticket_id: int) -> Ticket:
        ticket = cache.get_ticket(ticket_id)
        if ticket:
            return ticket
        raise TicketNotFoundError(ticket_id)

    async def save(self) -> None:
        cache.add_ticket(self)
        await execute_query(
            "INSERT INTO tickets (id, ticket_number, config, guild, user_, open) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT (id) DO UPDATE SET ticket_number = $2, config = $3, guild = $4, user_ = $5, open = $6 WHERE tickets.id = $1;",
            self.id,
            self.ticket_number,
            self.config_id,
            self.guild_id,
            self.user_id,
            self.open,
        )

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Ticket:
        try:
            ticket = cache.get_ticket(convert_int(argument))
            if ticket:
                return ticket
            raise TicketNotFoundError(argument)
        except ValueError:
            raise TicketNotFoundError(argument)

    def __int__(self) -> int:
        return self.id

    async def start(
        self,
        user: discord.Member,
        config: TicketConfig,
        *,
        response: Optional[discord.InteractionResponse] = None,
    ) -> None:
        from ...funcs import get_embed_author_member

        channel = user.guild.get_channel(self.id)
        if TYPE_CHECKING:
            assert isinstance(channel, discord.TextChannel)
        if response is not None:
            await response.send_message(
                ephemeral=True,
                embed=get_embed_author_member(
                    user, f"Check out your ticket here {channel.mention}!"
                ),
            )
        await channel.send(
            user.mention
            + "".join(f"<@{i}>" for i in (config.user_mentions or []))
            + "".join(f"<@&{i}>" for i in (config.role_mentions or [])),
            embed=get_embed_author_member(
                user,
                config.start_message.replace("\\n", "\n"),
                color=discord.Color.purple(),
            ),
        )


class TicketConfig:
    id: int
    category_id: Optional[int]
    guild_id: int
    start_message: str
    __slots__ = (
        "id",
        "category_id",
        "guild_id",
        "start_message",
        "archive_category_id",
        "role_mentions",
        "user_mentions",
    )

    def __init__(self, data: TicketConfigData) -> None:
        self.id = data["id"]
        self.category_id = data["category"]
        self.guild_id = data["guild"]
        self.start_message = data["start_message"]
        self.archive_category_id = data["archive_category"]
        self.role_mentions = data["role_mentions"]
        self.user_mentions = data["user_mentions"]

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> TicketConfig:
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        try:
            config = cache.get_ticket_config(convert_int(argument))
            if config and config.guild_id == ctx.guild.id:
                return config
            raise TicketConfigNotFoundError(argument)
        except ValueError:
            raise TicketConfigNotFoundError(argument)

    @classmethod
    async def fetch(cls, config_id: int) -> TicketConfig:
        config = cache.get_ticket_config(config_id)
        if config:
            return config
        raise TicketConfigNotFoundError(config_id)

    async def save(self) -> None:
        id = await execute_read_query(
            """INSERT INTO ticket_configs (category, guild, start_message, archive_category, role_mentions, user_mentions) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;""",
            self.category_id,
            self.guild_id,
            self.start_message,
            self.archive_category_id,
            self.role_mentions,
            self.user_mentions,
        )
        self.id = id[0]["id"]
        cache.add_ticket_config(self)

    async def create(self, user: discord.Member) -> Ticket:
        from ...errors import GuildNotFoundError
        from ...ref import bot

        guild = bot.get_guild(self.guild_id)
        if guild is None:
            raise GuildNotFoundError(self.guild_id)
        category = self.category_id and guild.get_channel(self.category_id)
        if TYPE_CHECKING and category is not None:
            assert isinstance(category, discord.CategoryChannel)
        number = (
            max(
                [i.ticket_number for i in cache.tickets if i.config_id == self.id]
                or [0]
            )
            + 1
        )
        if category is not None:
            overwrites = dict(category.overwrites.items())
            overwrites[user] = discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            )
        else:
            default_permissions = discord.PermissionOverwrite(
                **{
                    i: getattr(guild.default_role.permissions, i)
                    for i in dir(guild.default_role.permissions)
                    if isinstance(getattr(guild.default_role.permissions, i), bool)
                }
            )
            overwrites = {
                guild.default_role: default_permissions,
                user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                ),
            }
        channel = await guild.create_text_channel(
            f"ticket-{number}",
            overwrites=overwrites,
            category=category,
        )
        ticket = Ticket(
            {
                "id": channel.id,
                "ticket_number": number,
                "config": self.id,
                "guild": self.guild_id,
                "user_": user.id,
                "open": True,
            }
        )
        await ticket.save()
        return ticket

    def __int__(self) -> int:
        return self.id