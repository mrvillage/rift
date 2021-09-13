from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Union

import discord
from discord.ext import commands

from ...cache import cache
from ...errors import EmbassyConfigNotFoundError, EmbassyNotFoundError
from ..db import execute_query, execute_read_query
from ..get import get_embassy
from ..query import query_embassy_by_guild, query_embassy_config

__all__ = ("Embassy", "EmbassyConfig")

if TYPE_CHECKING:
    from typings import EmbassyConfigData, EmbassyData

    from .alliance import Alliance


class Embassy:
    __slots__ = (
        "embassy_id",
        "alliance_id",
        "config_id",
        "guild_id",
        "open",
    )

    def __init__(self, data: EmbassyData) -> None:
        self.embassy_id: int = data["embassy_id"]
        self.alliance_id: int = data["alliance_id"]
        self.config_id: int = data["config_id"]
        self.guild_id: int = data["guild_id"]
        self.open: bool = data["open"]

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> Embassy:
        try:
            embassy = cache.get_embassy(int(argument))
            if embassy:
                return embassy
            raise EmbassyNotFoundError(argument)
        except ValueError:
            raise EmbassyNotFoundError(argument)

    @classmethod
    async def fetch(cls, embassy_id: int) -> Embassy:
        embassy = cache.get_embassy(embassy_id)
        if embassy:
            return embassy
        raise EmbassyNotFoundError(embassy_id)

    def __int__(self) -> int:
        return self.embassy_id

    async def save(self) -> None:
        await execute_query(
            """INSERT INTO embassies (embassy_id, alliance_id, config_id, guild_id, open) VALUES ($1, $2, $3, $4, $5);""",
            self.embassy_id,
            self.alliance_id,
            self.config_id,
            self.guild_id,
            self.open,
        )

    async def delete(self) -> None:
        await execute_read_query(
            """DELETE FROM embassies WHERE embassy_id = $1;""", self.embassy_id
        )

    async def start(
        self,
        user: discord.Member,
        config: EmbassyConfig,
        *,
        response: discord.InteractionResponse = None,
    ) -> None:
        from ...funcs import get_embed_author_member

        channel = user.guild.get_channel(self.embassy_id)
        if TYPE_CHECKING:
            assert isinstance(channel, discord.TextChannel)
        if response is not None:
            await response.send_message(
                ephemeral=True,
                embed=get_embed_author_member(
                    user, f"Check out your embassy here {channel.mention}!"
                ),
            )
        await channel.send(
            user.mention,
            embed=get_embed_author_member(
                user, config.start_message.replace("\\n", "\n")
            ),
        )


class EmbassyConfig:
    __slots__ = (
        "config_id",
        "category_id",
        "guild_id",
        "start_message",
    )

    def __init__(self, data: EmbassyConfigData) -> None:
        self.config_id: int = data["config_id"]
        self.category_id: Optional[int] = data["category_id"]
        self.guild_id: int = data["guild_id"]
        self.start_message: str = data["start_message"]

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str) -> EmbassyConfig:
        try:
            config = cache.get_embassy_config(int(argument))
            if config:
                return config
            raise EmbassyConfigNotFoundError(argument)
        except ValueError:
            raise EmbassyConfigNotFoundError(argument)

    @classmethod
    async def fetch(cls, config_id: int) -> EmbassyConfig:
        config = cache.get_embassy_config(config_id)
        if config:
            return config
        raise EmbassyConfigNotFoundError(config_id)

    def __int__(self) -> int:
        return self.config_id

    async def save(self) -> None:
        await execute_read_query(
            """INSERT INTO embassy_configs (config_id, category_id, guild_id, start_message) VALUES ($1, $2, $3,$4);""",
            self.config_id,
            self.category_id,
            self.guild_id,
            self.start_message,
        )

    async def set_(self, **kwargs: Union[int, bool]) -> EmbassyConfig:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        await execute_query(
            f"""
        UPDATE embassy_configs SET {sets} WHERE config_id = $1;
        """,
            self.config_id,
            *args,
        )
        return self

    async def create(
        self, user: discord.Member, alliance: Alliance
    ) -> Tuple[Embassy, bool]:
        from ...errors import GuildNotFoundError
        from ...ref import bot

        embassies = await query_embassy_by_guild(self.guild_id)
        valid = [
            i
            for i in embassies
            if i["config_id"] == self.config_id and i["alliance_id"] == alliance.id
        ]
        if valid:
            embassy = await Embassy.fetch(valid[0]["embassy_id"])
            channel = bot.get_channel(embassy.embassy_id)
            if channel is None:
                await embassy.delete()
            else:
                if TYPE_CHECKING:
                    assert isinstance(channel, discord.TextChannel)
                await channel.set_permissions(
                    user, read_messages=True, send_messages=True
                )
                return embassy, False
        guild = bot.get_guild(self.guild_id)
        if guild is None:
            raise GuildNotFoundError(self.guild_id)
        category = self.category_id and guild.get_channel(self.category_id)
        if TYPE_CHECKING and category is not None:
            assert isinstance(category, discord.CategoryChannel)
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
            f"{alliance.id} {alliance.name}",
            overwrites=overwrites,
            category=category,
        )
        data = {
            "embassy_id": channel.id,
            "alliance_id": alliance.id,
            "config_id": self.config_id,
            "guild_id": self.guild_id,
            "open": True,
        }
        if TYPE_CHECKING:
            assert isinstance(data, EmbassyData)
        embassy = Embassy(data)
        await embassy.save()
        return embassy, True
