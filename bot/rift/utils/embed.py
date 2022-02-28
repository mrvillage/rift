from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import strings

__all__ = ("build_single_embed", "build_embed_from_user")

if TYPE_CHECKING:
    import datetime

    from quarrel import EmbedField


def build_single_embed(
    *,
    title: quarrel.Missing[str] = quarrel.MISSING,
    description: quarrel.Missing[str] = quarrel.MISSING,
    url: quarrel.Missing[str] = quarrel.MISSING,
    timestamp: quarrel.Missing[datetime.datetime] = quarrel.MISSING,
    color: quarrel.Missing[int] = quarrel.MISSING,
    author_name: quarrel.Missing[str] = quarrel.MISSING,
    author_url: quarrel.Missing[str] = quarrel.MISSING,
    author_icon_url: quarrel.Missing[str] = quarrel.MISSING,
    footer_text: quarrel.Missing[str] = quarrel.MISSING,
    provider_name: quarrel.Missing[str] = quarrel.MISSING,
    fields: quarrel.Missing[list[EmbedField]] = quarrel.MISSING,
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
    return embed


def build_embed_from_user(
    *,
    title: quarrel.Missing[str] = quarrel.MISSING,
    description: quarrel.Missing[str] = quarrel.MISSING,
    url: quarrel.Missing[str] = quarrel.MISSING,
    timestamp: quarrel.Missing[datetime.datetime] = quarrel.MISSING,
    color: quarrel.Missing[int] = quarrel.MISSING,
    author: quarrel.Member | quarrel.User,
    fields: quarrel.Missing[list[EmbedField]] = quarrel.MISSING,
) -> quarrel.Embed:
    return build_single_embed(
        title=title,
        description=description,
        url=url,
        timestamp=timestamp,
        color=color,
        author_name=author.username,
        author_icon_url=author.display_avatar.url,
        fields=fields,
    )
