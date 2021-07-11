from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod
from json import loads
from typing import Any, Mapping, Union

import discord

from ..db.sql import execute_query
from ..get import get_guild_settings, get_guild_welcome_settings
from .base import Base
from .nation import Nation


class BaseSettings(Base, ABC):
    @abstractmethod
    def __init__(self, data: Union[list, tuple]) -> None:
        ...

    @abstractclassmethod
    def default(cls: BaseSettings) -> BaseSettings:
        ...

    @abstractclassmethod
    async def fetch(cls: BaseSettings) -> BaseSettings:
        ...

    @abstractmethod
    async def set_(cls: BaseSettings, **kwargs: Mapping[str, Any]) -> BaseSettings:
        ...


class UserSettings(BaseSettings):
    def __init__(self) -> None:
        ...

    @classmethod
    async def default(cls: UserSettings) -> UserSettings:
        ...

    @classmethod
    async def fetch(cls) -> UserSettings:
        ...


class GuildWelcomeSettings(BaseSettings):
    def __init__(self: GuildWelcomeSettings, data: Union[list, tuple]) -> None:
        self.default = False
        self.welcome_data = data
        self.guild_id: int = int(data[0])
        self.welcome_message: Union[str, None] = data[1]
        self.welcome_channels: Union[list[int], None] = (
            loads(data[2]) if data[2] is not None else None
        )
        self.join_roles: Union[list[int], None] = (
            loads(data[3]) if data[3] is not None else None
        )
        self.verified_roles: Union[list[int], None] = (
            loads(data[4]) if data[4] is not None else None
        )
        self.member_roles: Union[list[int], None] = (
            loads(data[5]) if data[5] is not None else None
        )
        self.global_city_roles: Union[dict, None] = (
            loads(data[6]) if data[6] is not None else None
        )
        self.member_city_roles: Union[dict, None] = (
            loads(data[7]) if data[7] is not None else None
        )
        self.diplomat_roles: Union[dict, None] = (
            loads(data[8]) if data[8] is not None else None
        )
        self.alliance_roles: Union[dict, None] = (
            loads(data[9]) if data[9] is not None else None
        )
        self.alliance_gov_roles: Union[dict, None] = (
            loads(data[10]) if data[10] is not None else None
        )
        self.verified_nickname: Union[str, None] = (
            data[11] if data[11] is not None else None
        )

    @classmethod
    def default(cls: GuildWelcomeSettings, guild_id: int) -> GuildWelcomeSettings:
        settings = cls(
            (guild_id, None, "[]", "[]", "[]", "[]", "{}", "{}", "{}", "{}", "{}", None)
        )
        settings.default = True
        return settings

    @classmethod
    async def fetch(cls: GuildWelcomeSettings, guild_id: int) -> GuildWelcomeSettings:
        data = await get_guild_welcome_settings(guild_id)
        if data:
            return cls(data)
        return cls.default(guild_id)

    def format_welcome_embed(self, member: discord.Member, verified: bool):
        from ...funcs import get_embed_author_member

        if self.welcome_message:
            message = self.welcome_message.format(
                mention=member.author.mention,
                member=f"{member.author.name}#{member.author.discriminator}",
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
    ) -> str:
        await nation.make_attrs("alliance")
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

    async def set_(
        self: GuildWelcomeSettings, **kwargs: Mapping[str, Any]
    ) -> GuildWelcomeSettings:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        if self.default:
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


class GuildSettings(BaseSettings):
    welcome_settings: GuildWelcomeSettings

    def __init__(self, data: Union[list, tuple]) -> None:
        self.guild_id: int = data[0]
        ...

    async def _make_welcome_settings(self: GuildSettings) -> None:
        self.welcome_settings: GuildWelcomeSettings = await GuildWelcomeSettings.fetch(
            self.guild_id
        )

    @classmethod
    def default(cls: GuildSettings, guild_id: int) -> GuildSettings:
        settings = cls((guild_id, ...))
        settings.default = True
        return settings

    @classmethod
    async def fetch(cls: GuildSettings, guild_id: int, *attrs) -> GuildSettings:
        data = await get_guild_settings(guild_id)
        if data:
            settings: GuildSettings = cls(data)
        else:
            settings = cls.default(guild_id)
        await settings.make_attrs(*attrs)
        return settings

    async def set_(
        self: GuildWelcomeSettings, **kwargs: Mapping[str, Any]
    ) -> GuildWelcomeSettings:
        ...
