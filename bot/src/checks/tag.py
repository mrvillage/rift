from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import errors

__all__ = ("own_tag", "can_view_tag")

if TYPE_CHECKING:
    from .. import models
    from ..commands.common import CommonSlashCommand

    class TagOptions:
        tag: models.Tag
        __quarrel_raw_tag__: str


@quarrel.check(after_options=False, requires=["tag"])
async def own_tag(command: CommonSlashCommand[TagOptions]) -> bool:
    if command.interaction.user.id != command.options.tag.owner_id:
        raise errors.TagNotFoundError(
            command.interaction, command.options.__quarrel_raw_tag__
        )
    return True


@quarrel.check(after_options=False, requires=["tag"])
async def can_view_tag(command: CommonSlashCommand[TagOptions]) -> bool:
    if command.options.tag.can_use(command.interaction.user):
        return True
    raise errors.TagNotFoundError(
        command.interaction, command.options.__quarrel_raw_tag__
    )
