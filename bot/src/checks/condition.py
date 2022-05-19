from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import errors

__all__ = ("own_condition", "can_view_condition")

if TYPE_CHECKING:
    from .. import models
    from ..commands.common import CommonSlashCommand

    class ConditionOptions:
        condition: models.Condition
        __quarrel_raw_condition__: str


@quarrel.check(after_options=False, requires=["condition"])
async def own_condition(command: CommonSlashCommand[ConditionOptions]) -> bool:
    if command.interaction.user.id != command.options.condition.owner_id:
        raise errors.ConditionNotFoundError(
            command.interaction, command.options.__quarrel_raw_condition__
        )
    return True


@quarrel.check(after_options=False, requires=["condition"])
async def can_view_condition(command: CommonSlashCommand[ConditionOptions]) -> bool:
    if command.options.condition.can_use(command.interaction.user):
        return True
    raise errors.ConditionNotFoundError(
        command.interaction, command.options.__quarrel_raw_condition__
    )
