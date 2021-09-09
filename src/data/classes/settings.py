from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Union

import discord

from ..db.sql import execute_query
from ..get import get_guild_settings, get_guild_welcome_settings
from .base import Makeable
from .nation import Nation

__all__ = ("UserSettings", "GuildWelcomeSettings", "GuildSettings")

if TYPE_CHECKING:
    from typings import GuildSettingsData, GuildWelcomeSettingsData


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


class GuildWelcomeSettings(Makeable):
    __slots__ = (
        "guild_id",
        "welcome_message",
        "welcome_channels",
        "join_roles",
        "verified_roles",
        "member_roles",
        "global_city_roles",
        "member_city_roles",
        "diplomat_roles",
        "alliance_roles",
        "alliance_gov_roles",
        "verified_nickname",
        "defaulted",
    )

    def __init__(self, data: GuildWelcomeSettingsData) -> None:
        self.defaulted = False
        self.guild_id: int = int(data["guild_id"])
        self.welcome_message: Optional[str] = data["welcome_message"]
        self.welcome_channels: Optional[List[int]] = data["welcome_channels"]
        self.join_roles: Optional[List[int]] = data["join_roles"]
        self.verified_roles: Optional[List[int]] = data["verified_roles"]
        self.member_roles: Optional[List[int]] = data["member_roles"]
        self.global_city_roles: Optional[Dict[str, List[int]]] = data[
            "global_city_roles"
        ]
        self.member_city_roles: Optional[Dict[str, List[int]]] = data[
            "member_city_roles"
        ]
        self.diplomat_roles: Optional[Dict[str, List[int]]] = data["diplomat_roles"]
        self.alliance_roles: Optional[Dict[str, List[int]]] = data["alliance_roles"]
        self.alliance_gov_roles: Optional[Dict[str, List[int]]] = data[
            "alliance_gov_roles"
        ]
        self.verified_nickname: Optional[str] = data["verified_nickname"]

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
                "global_city_roles": None,
                "member_city_roles": None,
                "diplomat_roles": None,
                "alliance_roles": None,
                "alliance_gov_roles": None,
                "verified_nickname": None,
            }
        )
        settings.defaulted = True
        return settings

    @classmethod
    async def fetch(cls, guild_id: int) -> GuildWelcomeSettings:
        data = await get_guild_welcome_settings(guild_id)
        if data:
            return cls(data)
        return cls.default(guild_id)

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
            message += "\n\nIt doesn't look like you're verified! Be sure to run `?verify <nation>` to verify."
        return get_embed_author_member(member, message)

    async def set_verified_nickname(
        self, member: discord.Member, nation: Nation
    ) -> None:
        await nation.make_attrs("alliance")
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
        await member.edit(nick=nickname)

    async def set_(self, **kwargs: Any) -> GuildWelcomeSettings:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        if self.defaulted:
            await execute_query(
                f"""
            INSERT INTO guild_welcome_settings (guild_id, {', '.join(kwargs.keys())}) VALUES ({', '.join(f'${i}' for i in range(1, len(kwargs)+2))});
            """,
                str(self.guild_id),
                *tuple(kwargs.values()),
            )
        else:
            await execute_query(
                f"""
            UPDATE guild_welcome_settings SET {sets} WHERE guild_id = $1;
            """,
                str(self.guild_id),
                *args,
            )
        return self


class GuildSettings(Makeable):
    welcome_settings: GuildWelcomeSettings

    __slots__ = ("guild_id", "welcome_settings", "defaulted")

    def __init__(self, data: GuildSettingsData) -> None:
        self.guild_id: int = data["guild_id"]
        ...

    async def _make_welcome_settings(self) -> None:
        self.welcome_settings: GuildWelcomeSettings = await GuildWelcomeSettings.fetch(
            self.guild_id
        )

    @classmethod
    def default(cls, guild_id: int) -> GuildSettings:
        settings = cls((guild_id, ...))
        settings.defaulted = True
        return settings

    @classmethod
    async def fetch(cls, guild_id: int, *attrs) -> GuildSettings:
        data = await get_guild_settings(guild_id)
        if data:
            settings: GuildSettings = cls(data)
        else:
            settings = cls.default(guild_id)
        await settings.make_attrs(*attrs)
        return settings

    async def set_(self, **kwargs: Mapping[str, Any]) -> GuildSettings:
        ...
