from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import discord
from discord.ext import commands

from ...cache import cache
from ...errors import TicketConfigNotFoundError, TicketNotFoundError
from ..db import execute_query, execute_read_query

__all__ = ("Ticket", "TicketConfig")

if TYPE_CHECKING:
    from typings import TicketConfigData, TicketData


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
        self.config_id = data["config_id"]
        self.guild_id = data["guild_id"]
        self.user_id = data["user_id"]
        self.open = data["open"]

    @classmethod
    async def fetch(cls, ticket_id: int) -> Ticket:
        ticket = cache.get_ticket(ticket_id)
        if ticket:
            return ticket
        raise TicketNotFoundError(ticket_id)

    async def save(self) -> None:
        cache._tickets[self.id] = self
        await execute_read_query(
            """INSERT INTO tickets (id, ticket_number, config_id, guild_id, user_id, open) VALUES ($1, $2, $3, $4, $5, $6);""",
            self.id,
            self.ticket_number,
            self.config_id,
            self.guild_id,
            self.user_id,
            self.open,
        )

    async def set_(self, **kwargs: Union[int, bool]) -> Ticket:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        await execute_query(
            f"""
        UPDATE tickets SET {sets} WHERE id = $1;
        """,
            self.id,
            *args,
        )
        return self

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Ticket:
        ...

    def __int__(self) -> int:
        return self.id

    async def start(
        self,
        user: discord.Member,
        config: TicketConfig,
        *,
        response: discord.InteractionResponse = None,
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
            + "".join(f"<@{i}>" for i in config.user_mentions)
            + "".join(f"<@&{i}" for i in config.role_mentions),
            embed=get_embed_author_member(
                user, config.start_message.replace("\\n", "\n")
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
        self.category_id = data["category_id"]
        self.guild_id = data["guild_id"]
        self.start_message = data["start_message"]
        self.archive_category_id = data["archive_category_id"]
        self.role_mentions = data["role_mentions"]
        self.user_mentions = data["user_mentions"]

    @classmethod
    async def fetch(cls, config_id: int) -> TicketConfig:
        config = cache.get_ticket_config(config_id)
        if config:
            return config
        raise TicketConfigNotFoundError(config_id)

    async def save(self) -> None:
        cache._ticket_configs[self.id] = self
        await execute_query(
            """INSERT INTO ticket_configs (id, category_id, guild_id, start_message, archive_category_id) VALUES ($1, $2, $3, $4, $5, $6, $7);""",
            self.id,
            self.category_id,
            self.guild_id,
            self.start_message,
            self.archive_category_id,
            self.role_mentions,
            self.user_mentions,
        )

    async def set_(self, **kwargs: Union[int, bool]) -> TicketConfig:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        await execute_query(
            f"""
        UPDATE ticket_configs SET {sets} WHERE id = $1;
        """,
            self.id,
            *args,
        )
        return self

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
            max(i.ticket_number for i in cache.tickets if i.config_id == self.id) + 1
        )
        if category is not None:
            overwrites = {key: value for key, value in category.overwrites.items()}
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
        data = {
            "ticket_id": channel.id,
            "ticket_number": number,
            "config_id": self.id,
            "guild_id": self.guild_id,
            "user_id": user.id,
            "open": True,
        }
        if TYPE_CHECKING:
            assert isinstance(data, TicketData)
        ticket = Ticket(data)
        await ticket.save()
        return ticket

    def __int__(self) -> int:
        return self.id
