from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import strings

__all__ = (
    "build_single_embed",
    "build_single_embed_from_user",
    "build_single_embed_from_guild",
    "embed_field",
)

if TYPE_CHECKING:
    import datetime
    from typing import Any

    from quarrel import EmbedField, Missing


def build_single_embed(
    *,
    title: Missing[str] = quarrel.MISSING,
    description: Missing[str] = quarrel.MISSING,
    url: Missing[str] = quarrel.MISSING,
    timestamp: Missing[datetime.datetime] = quarrel.MISSING,
    color: Missing[int | quarrel.Color] = quarrel.MISSING,
    author_name: Missing[str] = quarrel.MISSING,
    author_url: Missing[str] = quarrel.MISSING,
    author_icon_url: Missing[str] = quarrel.MISSING,
    footer_text: Missing[str] = quarrel.MISSING,
    provider_name: Missing[str] = quarrel.MISSING,
    fields: Missing[list[EmbedField]] = quarrel.MISSING,
    image_url: Missing[str] = quarrel.MISSING,
    thumbnail_url: Missing[str] = quarrel.MISSING,
) -> quarrel.Embed:
    embed = quarrel.Embed(
        title=title, description=description, url=url, timestamp=timestamp, color=color
    )
    embed.author.name = author_name
    embed.author.url = author_url
    embed.author.icon_url = author_icon_url
    embed.footer.text = footer_text or strings.FOOTER_TEXT
    embed.provider.name = provider_name or strings.PROVIDER_NAME
    embed.fields = fields or []
    embed.image.url = image_url
    embed.thumbnail.url = thumbnail_url
    return embed


def build_single_embed_from_user(
    *,
    title: Missing[str] = quarrel.MISSING,
    description: Missing[str] = quarrel.MISSING,
    url: Missing[str] = quarrel.MISSING,
    timestamp: Missing[datetime.datetime] = quarrel.MISSING,
    color: Missing[int | quarrel.Color] = quarrel.MISSING,
    author: quarrel.Member | quarrel.User,
    author_url: Missing[str] = quarrel.MISSING,
    footer_text: Missing[str] = quarrel.MISSING,
    provider_name: Missing[str] = quarrel.MISSING,
    fields: Missing[list[EmbedField]] = quarrel.MISSING,
    image_url: Missing[str] = quarrel.MISSING,
    thumbnail_url: Missing[str] = quarrel.MISSING,
) -> quarrel.Embed:
    return build_single_embed(
        title=title,
        description=description,
        url=url,
        timestamp=timestamp,
        color=color,
        author_name=author.username,
        author_icon_url=author.display_avatar.url,
        author_url=author_url,
        footer_text=footer_text,
        provider_name=provider_name,
        fields=fields,
        image_url=image_url,
        thumbnail_url=thumbnail_url,
    )


def build_single_embed_from_guild(
    *,
    title: Missing[str] = quarrel.MISSING,
    description: Missing[str] = quarrel.MISSING,
    url: Missing[str] = quarrel.MISSING,
    timestamp: Missing[datetime.datetime] = quarrel.MISSING,
    color: Missing[int | quarrel.Color] = quarrel.MISSING,
    guild: quarrel.Guild,
    author_url: Missing[str] = quarrel.MISSING,
    footer_text: Missing[str] = quarrel.MISSING,
    provider_name: Missing[str] = quarrel.MISSING,
    fields: Missing[list[EmbedField]] = quarrel.MISSING,
    image_url: Missing[str] = quarrel.MISSING,
    thumbnail_url: Missing[str] = quarrel.MISSING,
) -> quarrel.Embed:
    return build_single_embed(
        title=title,
        description=description,
        url=url,
        timestamp=timestamp,
        color=color,
        author_name=guild.name,
        author_icon_url=guild.icon.url if guild.icon else quarrel.MISSING,
        author_url=author_url,
        footer_text=footer_text,
        provider_name=provider_name,
        fields=fields,
        image_url=image_url,
        thumbnail_url=thumbnail_url,
    )


def embed_field(
    name: Any, value: Any, inline: Missing[bool] = True
) -> quarrel.EmbedField:
    return quarrel.EmbedField(name=name, value=value, inline=inline)
