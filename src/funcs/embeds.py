from __future__ import annotations

from datetime import datetime

import discord
from typing import Sequence, Mapping, TYPE_CHECKING, Union, cast

from ..env import COLOR, FOOTER


def add_fields(
    embed: discord.Embed, fields: Sequence[Mapping[str, Union[bool, str]]]
) -> discord.Embed:
    for field in fields:
        if TYPE_CHECKING:
            assert isinstance(field["inline"], bool)
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=True if "inline" not in field else field["inline"],
        )
    return embed


def get_embed_author_member(
    member: Union[discord.Member, discord.User],
    description: Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
    color: Union[discord.Color, int] = COLOR,
    timestamp: datetime = None,
    footer: str = FOOTER,
    title: Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
    fields: Sequence[Mapping[str, str]] = [],
    image_url: Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
) -> discord.Embed:
    if isinstance(member, discord.Member):
        member = member._user
    return add_fields(
        discord.Embed(
            color=color,
            description=description,
            timestamp=timestamp or discord.utils.utcnow(),
            title=title,
        )
        .set_footer(text=footer)
        .set_author(
            name=f"{member.name}#{member.discriminator}",
            icon_url=str(member.avatar.url),
        )
        .set_image(url=image_url),
        fields,
    )


def get_embed_author_guild(
    guild: discord.Guild,
    description: Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
    color: Union[discord.Color, int] = COLOR,
    timestamp: datetime = None,
    footer: str = FOOTER,
    title: Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
    fields: Sequence[Mapping[str, str]] = [],
    image_url: Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
) -> discord.Embed:
    if TYPE_CHECKING:
        assert isinstance(guild.icon, discord.Asset)
    return add_fields(
        discord.Embed(
            color=color,
            description=description,
            timestamp=timestamp or discord.utils.utcnow(),
            title=title,
        )
        .set_footer(text=footer)
        .set_author(name=guild.name, icon_url=str(guild.icon.url))
        .set_image(url=image_url),
        fields,
    )
