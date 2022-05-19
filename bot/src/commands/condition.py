from __future__ import annotations

from typing import TYPE_CHECKING

from .. import cache, checks, embeds, models, options
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:
    from ..types.quarrel import MemberOrUser

    class ConditionCommandOptions:
        ...


class ConditionCommand(
    CommonSlashCommand["ConditionCommandOptions"],
    name="condition",
    description="Manage conditions.",
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class ConditionInfoCommandOptions:
        condition: models.Condition


class ConditionInfoCommand(
    CommonSlashCommand["ConditionInfoCommandOptions"],
    name="info",
    description="View information about a condition.",
    parent=ConditionCommand,
    options=[options.CONDITION],
    checks=[checks.can_view_condition],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_message(
            embed=self.options.condition.build_embed(self.interaction),
        )


if TYPE_CHECKING:

    class ConditionCreateCommandOptions:
        ...


class ConditionCreateCommand(
    CommonSlashCommand["ConditionCreateCommandOptions"],
    name="create",
    description="Create a condition.",
    parent=ConditionCommand,
    options=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class ConditionDeleteCommandOptions:
        condition: models.Condition


class ConditionDeleteCommand(
    CommonSlashCommand["ConditionDeleteCommandOptions"],
    name="delete",
    description="Delete a condition.",
    parent=ConditionCommand,
    options=[options.CONDITION],
    checks=[checks.own_condition],
):
    __slots__ = ()

    async def callback(self) -> None:
        cache.remove_condition(self.options.condition)
        await self.options.condition.delete()
        await self.interaction.respond_with_message(
            embed=embeds.condition_deleted(self.interaction, self.options.condition),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class ConditionEditCommandOptions:
        ...


class ConditionEditCommand(
    CommonSlashCommand["ConditionEditCommandOptions"],
    name="edit",
    description="Edit a condition.",
    parent=ConditionCommand,
    options=[],
    checks=[checks.own_condition],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class ConditionListCommandOptions:
        user: MemberOrUser


class ConditionListCommand(
    CommonSlashCommand["ConditionListCommandOptions"],
    name="list",
    description="List your conditions.",
    parent=ConditionCommand,
    options=[options.USER_DEFAULT_SELF],
):
    __slots__ = ()

    async def callback(self) -> None:
        conditions = sorted(
            {
                i
                for i in cache.conditions
                if i.owner_id == self.options.user.id
                and i.can_use(self.interaction.user)
            },
            key=lambda i: i.id,
        )
        await self.interaction.respond_with_message(
            embed=embeds.condition_list(self.interaction, conditions),
        )
