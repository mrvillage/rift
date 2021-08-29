from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import discord
from discord.ext import commands
from ..query import query_ticket_config

from ..db import execute_query, execute_read_query
from ..get import get_current_ticket_number, get_ticket

__all__ = ("Ticket", "TicketConfig")

if TYPE_CHECKING:
    from typings import TicketConfigData, TicketData


class Ticket:
    ticket_id: int
    ticket_number: int
    config_id: int
    guild_id: int
    user_id: int
    __slots__ = (
        "ticket_id",
        "ticket_number",
        "config_id",
        "guild_id",
        "user_id",
    )

    def __init__(self, data: TicketData) -> None:
        self.ticket_id = data["ticket_id"]
        self.ticket_number = data["ticket_number"]
        self.config_id = data["config_id"]
        self.guild_id = data["guild_id"]
        self.user_id = data["user_id"]
        self.open = data["open"]

    @classmethod
    async def fetch(cls, ticket_id: int) -> Ticket:
        return Ticket(await get_ticket(ticket_id=ticket_id))

    async def save(self) -> None:
        await execute_read_query(
            """INSERT INTO tickets (ticket_id, ticket_number, config_id, guild_id, user_id, open) VALUES ($1, $2, $3, $4, $5, $6);""",
            self.ticket_id,
            self.ticket_number,
            self.config_id,
            self.guild_id,
            self.user_id,
            self.open,
        )

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Ticket:
        ...

    def __int__(self) -> int:
        return self.ticket_id

    async def start(
        self,
        user: discord.Member,
        config: TicketConfig,
        *,
        response: discord.InteractionResponse = None,
    ) -> None:
        from ...funcs import get_embed_author_member

        channel = user.guild.get_channel(self.ticket_id)
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
            user.mention, embed=get_embed_author_member(user, config.start_message)
        )


class TicketConfig:
    config_id: int
    category_id: Optional[int]
    guild_id: int
    start_message: str
    __slots__ = (
        "config_id",
        "category_id",
        "guild_id",
        "start_message",
    )

    def __init__(self, data: TicketConfigData) -> None:
        self.config_id = data["config_id"]
        self.category_id = data["category_id"]
        self.guild_id = data["guild_id"]
        self.start_message = data["start_message"]

    @classmethod
    async def fetch(cls, config_id: int) -> TicketConfig:
        return TicketConfig(await query_ticket_config(config_id=config_id))

    async def save(self) -> None:
        await execute_query(
            """INSERT INTO ticket_configs (config_id, category_id, guild_id, start_message) VALUES ($1, $2, $3, $4);""",
            self.config_id,
            self.category_id,
            self.guild_id,
            self.start_message,
        )

    async def set_(self, **kwargs: Union[int, bool]) -> TicketConfig:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        await execute_query(
            f"""
        UPDATE ticket_configs SET {sets} WHERE config_id = $1;
        """,
            self.config_id,
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
        number = await get_current_ticket_number(self.config_id) + 1
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
            "config_id": self.config_id,
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
        return self.config_id
