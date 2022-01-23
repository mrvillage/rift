from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from .. import funcs
from ..env import COLOR, FOOTER
from .base import BaseError

if TYPE_CHECKING:
    from datetime import datetime
    from typing import List, Optional, Union

    from _typings import Field, MaybeEmptyEmbed

__all__ = (
    "Message",
    "EmbedMessage",
    "EmbedErrorMessage",
    "EmbedSuccessMessage",
    "EmbedInfoMessage",
)


class Message(BaseError):
    ...


class EmbedMessage(Message):
    def __init__(
        self,
        member: Union[discord.Member, discord.User],
        description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        color: Union[discord.Color, int] = COLOR,
        timestamp: Optional[datetime] = None,
        footer: str = FOOTER,
        title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        fields: List[Field] = [],
        image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        ephemeral: bool = False,
        success: bool = True,
    ) -> None:
        self.member: Union[discord.Member, discord.User] = member
        self.description: MaybeEmptyEmbed[str] = description
        self.color: Union[discord.Color, int] = color
        self.timestamp: Optional[datetime] = timestamp
        self.footer: str = footer
        self.title: MaybeEmptyEmbed[str] = title
        self.fields: List[Field] = fields
        self.image_url: MaybeEmptyEmbed[str] = image_url
        self.ephemeral: bool = ephemeral
        self.success: bool = success
        super().__init__()

    @property
    def embed(self) -> discord.Embed:
        return funcs.get_embed_author_member(
            member=self.member,
            description=self.description,
            color=self.color,
            timestamp=self.timestamp,
            footer=self.footer,
            title=self.title,
            fields=self.fields,
            image_url=self.image_url,
        )


class EmbedErrorMessage(EmbedMessage):
    def __init__(
        self,
        member: Union[discord.Member, discord.User],
        description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        timestamp: Optional[datetime] = None,
        footer: str = FOOTER,
        title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        fields: List[Field] = [],
        image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        ephemeral: bool = True,
        success: bool = True,
    ) -> None:
        super().__init__(
            member=member,
            description=description,
            color=discord.Color.red(),
            timestamp=timestamp,
            footer=footer,
            title=title,
            fields=fields,
            image_url=image_url,
            ephemeral=ephemeral,
            success=success,
        )


class EmbedSuccessMessage(EmbedMessage):
    def __init__(
        self,
        member: Union[discord.Member, discord.User],
        description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        timestamp: Optional[datetime] = None,
        footer: str = FOOTER,
        title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        fields: List[Field] = [],
        image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        ephemeral: bool = False,
        success: bool = True,
    ) -> None:
        super().__init__(
            member=member,
            description=description,
            color=discord.Color.red(),
            timestamp=timestamp,
            footer=footer,
            title=title,
            fields=fields,
            image_url=image_url,
            ephemeral=ephemeral,
            success=success,
        )


class EmbedInfoMessage(EmbedMessage):
    def __init__(
        self,
        member: Union[discord.Member, discord.User],
        description: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        timestamp: Optional[datetime] = None,
        footer: str = FOOTER,
        title: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        fields: List[Field] = [],
        image_url: MaybeEmptyEmbed[str] = discord.Embed.Empty,
        ephemeral: bool = False,
        success: bool = True,
    ) -> None:
        super().__init__(
            member=member,
            description=description,
            color=discord.Color.blue(),
            timestamp=timestamp,
            footer=footer,
            title=title,
            fields=fields,
            image_url=image_url,
            ephemeral=ephemeral,
            success=success,
        )
