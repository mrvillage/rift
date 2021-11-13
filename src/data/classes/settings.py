from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional, Set

import discord

from ...cache import cache
from ..db.sql import execute_query
from .alliance import Alliance
from .base import Makeable
from .nation import Nation

__all__ = (
    "UserSettings",
    "AllianceAutoRole",
    "GuildWelcomeSettings",
    "GuildSettings",
    "AllianceSettings",
)

if TYPE_CHECKING:
    from _typings import (
        AllianceAutoRoleData,
        AllianceSettingsData,
        GuildSettingsData,
        GuildWelcomeSettingsData,
    )


class UserSettings(Makeable):
    __slots__ = ()

    def __init__(self) -> None:
        ...

    @classmethod
    async def default(cls) -> UserSettings:
        ...

    @classmethod
    async def fetch(cls) -> UserSettings:
        ...


class AllianceAutoRole:
    __slots__ = ("role_id", "guild_id", "alliance_id")

    def __init__(self, data: AllianceAutoRoleData) -> None:
        self.role_id: int = data["role_id"]
        self.guild_id: int = data["guild_id"]
        self.alliance_id: int = data["alliance_id"]

    @classmethod
    async def create(cls, role: discord.Role, alliance: Alliance) -> AllianceAutoRole:
        await execute_query(
            "INSERT INTO alliance_auto_roles (role_id, guild_id, alliance_id) VALUES ($1, $2, $3);",
            role.id,
            role.guild.id,
            alliance.id,
        )
        auto = cls(
            {"role_id": role.id, "guild_id": role.guild.id, "alliance_id": alliance.id}
        )
        cache.add_alliance_auto_role(auto)
        return auto

    async def delete(self) -> None:
        cache.remove_alliance_auto_role(self)
        await execute_query(
            "DELETE FROM alliance_auto_roles WHERE role_id = $1 AND guild_id = $2 AND alliance_id = $3;",
            self.role_id,
            self.guild_id,
            self.alliance_id,
        )

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    def __str__(self) -> str:
        return f"<@&{self.role_id}> - {self.alliance}"


class GuildWelcomeSettings(Makeable):
    __slots__ = (
        "guild_id",
        "welcome_message",
        "welcome_channels",
        "join_roles",
        "verified_roles",
        "member_roles",
        "diplomat_roles",
        "verified_nickname",
        "defaulted",
    )

    def __init__(self, data: GuildWelcomeSettingsData) -> None:
        self.defaulted: bool = False
        self.guild_id: int = int(data["guild_id"])
        self.welcome_message: Optional[str] = data["welcome_message"]
        self.welcome_channels: Optional[List[int]] = data["welcome_channels"]
        self.join_roles: Optional[List[int]] = data["join_roles"]
        self.verified_roles: Optional[List[int]] = data["verified_roles"]
        self.member_roles: Optional[List[int]] = data["member_roles"]
        self.diplomat_roles: Optional[List[int]] = data["diplomat_roles"]
        self.verified_nickname: Optional[str] = data["verified_nickname"]
        self.enforce_verified_nickname: bool = (
            data["enforce_verified_nickname"]
            if data["enforce_verified_nickname"] is not None
            else False
        )
        self.alliance_auto_roles_enabled: bool = (
            data["alliance_auto_roles_enabled"]
            if data["alliance_auto_roles_enabled"] is not None
            else False
        )
        self.alliance_auto_role_creation_enabled: bool = (
            data["alliance_auto_role_creation_enabled"]
            if data["alliance_auto_role_creation_enabled"] is not None
            else False
        )

    @classmethod
    def default(cls, guild_id: int) -> GuildWelcomeSettings:
        settings = cls(
            {
                "guild_id": guild_id,
                "welcome_message": None,
                "welcome_channels": None,
                "join_roles": None,
                "verified_roles": None,
                "member_roles": None,
                "diplomat_roles": None,
                "verified_nickname": None,
                "enforce_verified_nickname": None,
                "alliance_auto_roles_enabled": None,
                "alliance_auto_role_creation_enabled": None,
            }
        )
        settings.defaulted = True
        return settings

    @classmethod
    async def fetch(cls, guild_id: int) -> GuildWelcomeSettings:
        return cache.get_guild_welcome_settings(guild_id) or cls.default(guild_id)

    @property
    def alliance_auto_roles(self) -> Set[AllianceAutoRole]:
        return {i for i in cache.alliance_auto_roles if i.guild_id == self.guild_id}

    def format_welcome_embed(self, member: discord.Member, verified: bool):
        from ...funcs import get_embed_author_member

        if self.welcome_message:
            message = self.welcome_message.format(
                mention=member.mention,
                member=f"{member.name}#{member.discriminator}",
                guild=member.guild.name,
                server=member.guild.name,
            )
        else:
            message = f"Welcome to {member.guild.name}!"
        if not verified:
            message += "\n\nIt doesn't look like you're linked! Be sure to run `/link` and provide your nation to get linked."
        return get_embed_author_member(member, message, color=discord.Color.blue())

    def format_verified_nickname(
        self, member: discord.Member, nation: Nation
    ) -> Optional[str]:
        if not self.verified_nickname:
            return
        if nation.alliance:
            nickname = self.verified_nickname.format(
                nation_name=nation.name,
                nation_id=str(nation.id),
                leader_name=nation.leader,
                alliance_name=nation.alliance.name,
                alliance_id=str(nation.alliance.id),
                alliance_acronym=nation.alliance.acronym,
            )
        else:
            nickname = self.verified_nickname.format(
                nation_name=nation.name,
                nation_id=nation.id,
                leader_name=nation.leader,
                alliance_name=None,
                alliance_id=0,
                alliance_acronym="NA",
            )
        nickname = nickname.format(
            member_name=member.name,
            member_username=f"{member.name}#{member.discriminator}",
            member_discriminator=member.discriminator,
        )
        nickname = nickname[:32]

    async def set_verified_nickname(
        self, member: discord.Member, nation: Nation
    ) -> None:
        nickname = self.format_verified_nickname(member, nation)
        if nickname is None:
            return
        await member.edit(nick=nickname)

    async def set_(self, **kwargs: Any) -> GuildWelcomeSettings:
        for key, value in kwargs.items():
            setattr(self, key, value)
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        if self.defaulted:
            await execute_query(
                f"""
            INSERT INTO guild_welcome_settings (guild_id, {', '.join(kwargs.keys())}) VALUES ({', '.join(f'${i}' for i in range(1, len(kwargs)+2))});
            """,
                self.guild_id,
                *tuple(kwargs.values()),
            )
            cache.add_guild_welcome_settings(self)
            self.defaulted = False
        else:
            await execute_query(
                f"""
            UPDATE guild_welcome_settings SET {sets} WHERE guild_id = $1;
            """,
                self.guild_id,
                *args,
            )
        return self


class GuildSettings(Makeable):
    __slots__ = (
        "guild_id",
        "defaulted",
        "purpose",
        "purpose_argument",
    )

    def __init__(self, data: GuildSettingsData) -> None:
        self.defaulted: bool = False
        self.guild_id: int = data["guild_id"]
        self.purpose: Optional[str] = data["purpose"]
        self.purpose_argument: Optional[str] = data["purpose_argument"]
        self.manager_role_ids: Optional[List[int]] = data["manager_role_ids"]

    @cached_property
    def welcome_settings(self) -> GuildWelcomeSettings:
        return cache.get_guild_welcome_settings(
            self.guild_id
        ) or GuildWelcomeSettings.default(self.guild_id)

    @classmethod
    def default(cls, guild_id: int) -> GuildSettings:
        settings = cls(
            {
                "guild_id": guild_id,
                "purpose": None,
                "purpose_argument": None,
                "manager_role_ids": None,
            }
        )
        settings.defaulted = True
        return settings

    @classmethod
    async def fetch(cls, guild_id: int, *attrs: str) -> GuildSettings:
        return cache.get_guild_settings(guild_id) or cls.default(guild_id)

    async def set_(self, **kwargs: Any) -> GuildSettings:
        for key, value in kwargs.items():
            setattr(self, key, value)
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        if self.defaulted:
            await execute_query(
                f"""
            INSERT INTO guild_settings (guild_id, {', '.join(kwargs.keys())}) VALUES ({', '.join(f'${i}' for i in range(1, len(kwargs)+2))});
            """,
                self.guild_id,
                *tuple(kwargs.values()),
            )
            cache.add_guild_settings(self)
            self.defaulted = False
        else:
            await execute_query(
                f"""
            UPDATE guild_settings SET {sets} WHERE guild_id = $1;
            """,
                self.guild_id,
                *args,
            )
        return self


class AllianceSettings:
    __slots__ = (
        "alliance_id",
        "defaulted",
        "default_raid_condition",
        "default_nuke_condition",
        "default_military_condition",
    )

    def __init__(self, data: AllianceSettingsData) -> None:
        self.defaulted: bool = False
        self.alliance_id: int = data["alliance_id"]
        self.default_raid_condition: Optional[str] = data["default_raid_condition"]
        self.default_nuke_condition: Optional[str] = data["default_nuke_condition"]
        self.default_military_condition: Optional[str] = data[
            "default_military_condition"
        ]

    @classmethod
    def default(cls, alliance_id: int, /) -> AllianceSettings:
        settings = cls(
            {
                "alliance_id": alliance_id,
                "default_raid_condition": None,
                "default_nuke_condition": None,
                "default_military_condition": None,
            }
        )
        settings.defaulted = True
        return settings

    @classmethod
    async def fetch(cls, alliance_id: int) -> AllianceSettings:
        return cache.get_alliance_settings(alliance_id) or cls.default(alliance_id)

    async def set_(self, **kwargs: Any) -> AllianceSettings:
        for key, value in kwargs.items():
            setattr(self, key, value)
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        if self.defaulted:
            await execute_query(
                f"""
            INSERT INTO alliance_settings (alliance_id, {', '.join(kwargs.keys())}) VALUES ({', '.join(f'${i}' for i in range(1, len(kwargs)+2))});
            """,
                self.alliance_id,
                *tuple(kwargs.values()),
            )
            cache.add_alliance_settings(self)
            self.defaulted = False
        else:
            await execute_query(
                f"""
            UPDATE alliance_settings SET {sets} WHERE alliance_id = $1;
            """,
                self.alliance_id,
                *args,
            )
        return self
