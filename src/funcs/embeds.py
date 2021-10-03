from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union

import discord

from _typings import Field, MaybeEmptyEmbed

from ..env import COLOR, FOOTER

__all__ = ("get_embed_author_member", "get_embed_author_guild")


def add_fields(embed: discord.Embed, fields: List[Field]) -> discord.Embed:
    for field in fields:
        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field.get("inline", True),
        )
    return embed


def get_embed_author_member(
    member: Union[discord.Member, discord.User],
    description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
    color: Union[discord.Color, int] = COLOR,
    timestamp: Optional[datetime] = None,
    footer: str = FOOTER,
    title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
    fields: List[Field] = [],
    image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
) -> discord.Embed:
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
            icon_url=str(member.display_avatar.url),
        )
        .set_image(url=image_url),
        fields,
    )


def get_embed_author_guild(
    guild: discord.Guild,
    description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
    color: Union[discord.Color, int] = COLOR,
    timestamp: Optional[datetime] = None,
    footer: str = FOOTER,
    title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
    fields: List[Field] = [],
    image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
) -> discord.Embed:
    return add_fields(
        discord.Embed(
            color=color,
            description=description,
            timestamp=timestamp or discord.utils.utcnow(),
            title=title,
        )
        .set_footer(text=footer)
        .set_author(
            name=guild.name,
            icon_url=(guild.icon and guild.icon.url) or discord.Embed.Empty,
        )
        .set_image(url=image_url),
        fields,
    )
