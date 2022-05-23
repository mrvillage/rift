from __future__ import annotations

from typing import TYPE_CHECKING

from .. import cache, checks, embeds, models, options
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:
    from quarrel import Missing

    from ..types.quarrel import MemberOrUser

    class ConditionCommandOptions:
        ...


@bot.command
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
        name: str
        expression: models.Condition
        public: bool
        use_condition: Missing[models.Condition]


class ConditionCreateCommand(
    CommonSlashCommand["ConditionCreateCommandOptions"],
    name="create",
    description="Create a condition.",
    parent=ConditionCommand,
    options=[
        options.NAME,
        options.EXPRESSION,
        options.PUBLIC_DEFAULT_FALSE,
        options.USE_CONDITION_OPTIONAL,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.expression.edit(
            self.options.name,
            self.options.expression.get_expression(),
            self.options.public,
            self.options.use_condition and self.options.use_condition.get_expression(),
            self.interaction.user.id,
        )
        cache.add_condition(self.options.expression)
        await self.interaction.respond_with_message(
            embed=embeds.condition_created(self.interaction, self.options.expression),
            ephemeral=True,
        )


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
        condition: models.Condition
        name: Missing[str]
        expression: Missing[models.Condition]
        public: Missing[bool]
        use_condition: Missing[models.Condition]


class ConditionEditCommand(
    CommonSlashCommand["ConditionEditCommandOptions"],
    name="edit",
    description="Edit a condition.",
    parent=ConditionCommand,
    options=[
        options.CONDITION,
        options.NAME_OPTIONAL,
        options.EXPRESSION_OPTIONAL,
        options.PUBLIC_OPTIONAL,
        options.USE_CONDITION_OPTIONAL,
    ],
    checks=[checks.own_condition],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.condition.edit(
            self.options.name,
            self.options.expression and self.options.expression.get_expression(),
            self.options.public,
            self.options.use_condition and self.options.use_condition.get_expression(),
        )
        await self.interaction.respond_with_message(
            embed=embeds.condition_edited(self.interaction, self.options.condition),
            ephemeral=True,
        )


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
