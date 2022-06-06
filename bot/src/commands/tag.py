from __future__ import annotations

from typing import TYPE_CHECKING

from .. import cache, checks, components, embeds, models, options
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:

    class TagCommandOptions:
        ...


@bot.command
class TagCommand(
    CommonSlashCommand["TagCommandOptions"],
    name="tag",
    description="Manage tags.",
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TagInfoCommandOptions:
        tag: models.Tag


class TagInfoCommand(
    CommonSlashCommand["TagInfoCommandOptions"],
    name="info",
    description="View information about a tag.",
    parent=TagCommand,
    options=[options.TAG],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_message(
            embed=self.options.tag.build_embed(self.interaction),
        )


if TYPE_CHECKING:

    class TagCreateCommandOptions:
        ...


class TagCreateCommand(
    CommonSlashCommand["TagCreateCommandOptions"],
    name="create",
    description="Create a tag.",
    parent=TagCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_modal(modal=components.TagCreateModal())


if TYPE_CHECKING:

    class TagDeleteCommandOptions:
        tag: models.Tag


class TagDeleteCommand(
    CommonSlashCommand["TagDeleteCommandOptions"],
    name="delete",
    description="Delete a tag.",
    parent=TagCommand,
    options=[options.TAG],
    checks=[checks.own_tag],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.tag.delete()
        await self.interaction.respond_with_message(
            embed=embeds.tag_deleted(self.interaction, self.options.tag),
        )


if TYPE_CHECKING:

    class TagEditCommandOptions:
        tag: models.Tag


class TagEditCommand(
    CommonSlashCommand["TagEditCommandOptions"],
    name="edit",
    description="Edit a tag.",
    parent=TagCommand,
    options=[options.TAG],
    checks=[checks.own_tag],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_modal(modal=components.TagEditModal(self.options.tag))


if TYPE_CHECKING:

    class TagListCommandOptions:
        ...


class TagListCommand(
    CommonSlashCommand["TagListCommandOptions"],
    name="list",
    description="List tags.",
    parent=TagCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        user = self.interaction.user
        tags = [i for i in cache.tags if i.can_use(user)]
        await self.interaction.respond_with_message(
            embed=embeds.tag_list(self.interaction, tags),
        )


if TYPE_CHECKING:

    class TagSendCommandOptions:
        tag: models.Tag


class TagSendCommand(
    CommonSlashCommand["TagSendCommandOptions"],
    name="send",
    description="Send a tag.",
    parent=TagCommand,
    options=[options.TAG],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_message(
            embed=self.options.tag.build_display_embed(self.interaction),
        )
