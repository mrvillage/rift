from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Set

import discord

from ...cache import cache
from ...ref import bot
from ..db.sql import execute_query
from .alliance import Alliance
from .base import Makeable
from .nation import Nation

__all__ = (
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


class AllianceAutoRole:
    __slots__ = ("role_id", "guild_id", "alliance_id")

    def __init__(self, data: AllianceAutoRoleData) -> None:
        self.role_id: int = data["role"]
        self.guild_id: int = data["guild"]
        self.alliance_id: int = data["alliance"]

    @classmethod
    async def create(cls, role: discord.Role, alliance: Alliance) -> AllianceAutoRole:
        auto = cls({"role": role.id, "guild": role.guild.id, "alliance": alliance.id})
        await auto.save()
        cache.add_alliance_auto_role(auto)
        return auto

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO alliance_auto_roles (role, guild, alliance) VALUES ($1, $2, $3);",
            self.role_id,
            self.guild_id,
            self.alliance_id,
        )

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
        "enforce_verified_nickname",
        "alliance_auto_roles_enabled",
        "alliance_auto_role_creation_enabled",
    )

    def __init__(self, data: GuildWelcomeSettingsData) -> None:
        self.guild_id: int = int(data["guild"])
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
            else True
        )

    @classmethod
    def default(cls, guild_id: int) -> GuildWelcomeSettings:
        return cls(
            {
                "guild": guild_id,
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
        if not verified and not member.bot:
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

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO guild_welcome_settings (guild, welcome_message, welcome_channels, join_roles, verified_roles, member_roles, diplomat_roles, verified_nickname, enforce_verified_nickname, alliance_auto_roles_enabled, alliance_auto_role_creation_enabled) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) ON CONFLICT (guild) DO UPDATE SET welcome_message = $2, welcome_channels = $3, join_roles = $4, verified_roles = $5, member_roles = $6, diplomat_roles = $7, verified_nickname = $8, enforce_verified_nickname = $9, alliance_auto_roles_enabled = $10, alliance_auto_role_creation_enabled = $11 WHERE guild_welcome_settings.guild = $1;",
            self.guild_id,
            self.welcome_message,
            self.welcome_channels,
            self.join_roles,
            self.verified_roles,
            self.member_roles,
            self.diplomat_roles,
            self.verified_nickname,
            self.enforce_verified_nickname,
            self.alliance_auto_roles_enabled,
            self.alliance_auto_role_creation_enabled,
        )


class GuildSettings(Makeable):
    __slots__ = (
        "guild_id",
        "defaulted",
        "purpose",
        "purpose_argument",
        "manager_role_ids",
    )

    def __init__(self, data: GuildSettingsData) -> None:
        self.defaulted: bool = False
        self.guild_id: int = data["guild"]
        self.purpose: Optional[str] = data["purpose"]
        self.purpose_argument: Optional[str] = data["purpose_argument"]
        self.manager_role_ids: Optional[List[int]] = data["manager_role_ids"]

    @property
    def welcome_settings(self) -> GuildWelcomeSettings:
        return cache.get_guild_welcome_settings(
            self.guild_id
        ) or GuildWelcomeSettings.default(self.guild_id)

    @classmethod
    def default(cls, guild_id: int) -> GuildSettings:
        settings = cls(
            {
                "guild": guild_id,
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

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO guild_settings (guild, purpose, purpose_argument, manager_role_ids) VALUES ($1, $2, $3, $4) ON CONFLICT (guild) DO UPDATE SET purpose = $2, purpose_argument = $3, manager_role_ids = $4 WHERE guild_settings.guild = $1;",
            self.guild_id,
            self.purpose,
            self.purpose_argument,
            self.manager_role_ids,
        )


class AllianceSettings:
    __slots__ = (
        "alliance_id",
        "default_raid_condition",
        "default_nuke_condition",
        "default_military_condition",
        "default_attack_raid_condition",
        "default_attack_nuke_condition",
        "default_attack_military_condition",
        "withdraw_channels",
        "require_withdraw_approval",
        "offshore_id",
        "withdraw_from_offshore",
    )

    def __init__(self, data: AllianceSettingsData) -> None:
        self.alliance_id: int = data["alliance"]
        self.default_raid_condition: Optional[str] = data["default_raid_condition"]
        self.default_nuke_condition: Optional[str] = data["default_nuke_condition"]
        self.default_military_condition: Optional[str] = data[
            "default_military_condition"
        ]
        self.default_attack_raid_condition: Optional[str] = data[
            "default_attack_raid_condition"
        ]
        self.default_attack_nuke_condition: Optional[str] = data[
            "default_attack_nuke_condition"
        ]
        self.default_attack_military_condition: Optional[str] = data[
            "default_attack_military_condition"
        ]
        self.withdraw_channels: Optional[List[int]] = data["withdraw_channels"]
        self.require_withdraw_approval: bool = data["require_withdraw_approval"]
        self.offshore_id: Optional[int] = data["offshore"]
        self.withdraw_from_offshore: bool = data["withdraw_from_offshore"]

    @classmethod
    def default(cls, alliance_id: int, /) -> AllianceSettings:
        return cls(
            {
                "alliance": alliance_id,
                "default_raid_condition": None,
                "default_nuke_condition": None,
                "default_military_condition": None,
                "default_attack_raid_condition": None,
                "default_attack_nuke_condition": None,
                "default_attack_military_condition": None,
                "withdraw_channels": None,
                "require_withdraw_approval": True,
                "offshore": None,
                "withdraw_from_offshore": False,
            }
        )

    @classmethod
    async def fetch(cls, alliance_id: int) -> AllianceSettings:
        return cache.get_alliance_settings(alliance_id) or cls.default(alliance_id)

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO alliance_settings (alliance, default_raid_condition, default_nuke_condition, default_military_condition, default_attack_raid_condition, default_attack_nuke_condition, default_attack_military_condition, withdraw_channels, require_withdraw_approval) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT (alliance) DO UPDATE SET default_raid_condition = $2, default_nuke_condition = $3, default_military_condition = $4, default_attack_raid_condition = $5, default_attack_nuke_condition = $6, default_attack_military_condition = $7, withdraw_channels = $8, require_withdraw_approval = $9, offshore = $10, withdraw_from_offshore = $11 WHERE alliance_settings.alliance = $1;",
            self.alliance_id,
            self.default_raid_condition,
            self.default_nuke_condition,
            self.default_military_condition,
            self.default_attack_raid_condition,
            self.default_attack_nuke_condition,
            self.default_attack_military_condition,
            self.withdraw_channels,
            self.require_withdraw_approval,
            self.offshore_id,
            self.withdraw_from_offshore,
        )

    @property
    def withdraw_channels_(self) -> List[discord.TextChannel]:
        if self.withdraw_channels is None:
            return []
        return [
            c
            for i in self.withdraw_channels
            if (c := bot.get_channel(i)) is not None
            and isinstance(c, discord.TextChannel)
        ]

    @property
    def offshore(self) -> Optional[Alliance]:
        return cache.get_alliance(self.offshore_id or -1)
