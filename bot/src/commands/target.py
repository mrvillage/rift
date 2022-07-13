from __future__ import annotations

from typing import TYPE_CHECKING

import lang
import quarrel

from .. import cache, components, embeds, models, options, utils
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:

    class TargetCommandOptions:
        ...


@bot.command
class TargetCommand(
    CommonSlashCommand["TargetCommandOptions"],
    name="target",
    description="Manage target reminders and find targets.",
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetFindCommandOptions:
        config: quarrel.Missing[models.TargetConfig]
        rater: quarrel.Missing[models.TargetRater]
        attack: bool
        expression: quarrel.Missing[lang.Expression]
        nation: models.Nation
        use_config_condition: bool


class TargetFindCommand(
    CommonSlashCommand["TargetFindCommandOptions"],
    name="find",
    description="Find targets.",
    parent=TargetCommand,
    options=[
        options.TARGET_CONFIG_OPTIONAL,
        options.TARGET_RATER_OPTIONAL,
        options.TARGET_FIND_ATTACK_OPTIONAL,
        options.EXPRESSION_OPTIONAL,
        options.NATION_DEFAULT_SELF,
        options.USE_TARGET_CONFIG_CONDITION,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        config = self.options.config
        rater = (
            self.options.rater
            or (config and cache.get_target_rater(config.rater))
            or models.TargetRater.default_rater()
        )
        if config:
            await self.interaction.respond(
                quarrel.InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            )
            targets = config.find_targets(
                config.count,
                rater,
                config.attack
                if self.options.attack is quarrel.MISSING
                else self.options.attack,
                lang.parse_expression(config.condition)
                if self.options.expression is quarrel.MISSING
                else utils.merge_expressions(
                    self.options.expression, config.condition, sep="&&"
                )
                if self.options.use_config_condition
                else self.options.expression,
                self.options.nation,
            )
            await self.interaction.edit_original_response(
                embed=embeds.targets(self.interaction, targets, 1, self.options.nation),
                grid=components.TargetsGrid(self.interaction.user.id, targets, 1),
            )
        else:
            await self.interaction.respond_with_message(
                embed=embeds.target_find_wizard(self.interaction),
                grid=components.TargetFindGrid(
                    self.interaction.user.id,
                    rater,
                    self.options.attack,
                    self.options.expression,
                    self.options.nation,
                ),
            )


if TYPE_CHECKING:

    class TargetConfigCommandOptions:
        ...


class TargetConfigCommand(
    CommonSlashCommand["TargetConfigCommandOptions"],
    name="config",
    description="Manage target configs.",
    parent=TargetCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetConfigInfoCommandOptions:
        config: models.TargetConfig


class TargetConfigInfoCommand(
    CommonSlashCommand["TargetConfigInfoCommandOptions"],
    name="info",
    description="View information about a target config.",
    parent=TargetConfigCommand,
    options=[options.TARGET_CONFIG],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetConfigCreateCommandOptions:
        name: quarrel.Missing[str]
        rater: quarrel.Missing[models.TargetRater]
        condition: quarrel.Missing[models.Condition]
        use_condition: quarrel.Missing[models.Condition]
        attack: bool


class TargetConfigCreateCommand(
    CommonSlashCommand["TargetConfigCreateCommandOptions"],
    name="create",
    description="Create a target config.",
    parent=TargetConfigCommand,
    options=[
        options.NAME_OPTIONAL,
        options.TARGET_RATER_OPTIONAL,
        options.CONDITION_OPTIONAL,
        options.USE_CONDITION_OPTIONAL,
        options.TARGET_FIND_ATTACK,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...  # for count use flags and a followup message with a select menu (will have options for everything in the rater)


if TYPE_CHECKING:

    class TargetConfigDeleteCommandOptions:
        config: models.TargetConfig


class TargetConfigDeleteCommand(
    CommonSlashCommand["TargetConfigDeleteCommandOptions"],
    name="delete",
    description="Delete a target config.",
    parent=TargetConfigCommand,
    options=[options.TARGET_CONFIG],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetConfigEditCommandOptions:
        config: models.TargetConfig
        name: quarrel.Missing[str]
        rater: quarrel.Missing[models.TargetRater]
        condition: quarrel.Missing[models.Condition]
        use_condition: quarrel.Missing[models.Condition]
        attack: quarrel.Missing[bool]


class TargetConfigEditCommand(
    CommonSlashCommand["TargetConfigEditCommandOptions"],
    name="edit",
    description="Edit a target config.",
    parent=TargetConfigCommand,
    options=[
        options.TARGET_CONFIG,
        options.NAME_OPTIONAL,
        options.TARGET_RATER_OPTIONAL,
        options.CONDITION_OPTIONAL,
        options.USE_CONDITION_OPTIONAL,
        options.TARGET_FIND_ATTACK_OPTIONAL,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetConfigListCommandOptions:
        user: quarrel.User | quarrel.Member


class TargetConfigListCommand(
    CommonSlashCommand["TargetConfigListCommandOptions"],
    name="list",
    description="List your target configs.",
    parent=TargetConfigCommand,
    options=[options.USER_OPTIONAL],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetRaterCommandOptions:
        ...


class TargetRaterCommand(
    CommonSlashCommand["TargetRaterCommandOptions"],
    name="rater",
    description="Manage target raters.",
    parent=TargetCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetRaterInfoCommandOptions:
        rater: models.TargetRater


class TargetRaterInfoCommand(
    CommonSlashCommand["TargetRaterInfoCommandOptions"],
    name="info",
    description="View information about a target rater.",
    parent=TargetRaterCommand,
    options=[options.TARGET_RATER],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetRaterCreateCommandOptions:
        base_rater: models.TargetRater
        cities: quarrel.Missing[models.Condition]
        infrastructure: quarrel.Missing[models.Condition]
        activity: quarrel.Missing[models.Condition]
        soldiers: quarrel.Missing[models.Condition]
        tanks: quarrel.Missing[models.Condition]
        aircraft: quarrel.Missing[models.Condition]
        ships: quarrel.Missing[models.Condition]
        missiles: quarrel.Missing[models.Condition]
        nukes: quarrel.Missing[models.Condition]
        money: quarrel.Missing[models.Condition]
        coal: quarrel.Missing[models.Condition]
        oil: quarrel.Missing[models.Condition]
        uranium: quarrel.Missing[models.Condition]
        iron: quarrel.Missing[models.Condition]
        bauxite: quarrel.Missing[models.Condition]
        lead: quarrel.Missing[models.Condition]
        gasoline: quarrel.Missing[models.Condition]
        munitions: quarrel.Missing[models.Condition]
        steel: quarrel.Missing[models.Condition]
        aluminum: quarrel.Missing[models.Condition]
        food: quarrel.Missing[models.Condition]


class TargetRaterCreateCommand(
    CommonSlashCommand["TargetRaterCreateCommandOptions"],
    name="create",
    description="Create a target rater.",
    parent=TargetRaterCommand,
    options=[options.BASE_TARGET_RATER_OPTIONAL, *options.TARGET_RATER_ATTRIBUTES],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...  # either a base rater needs to be provided (that will fill in the extra attributes) or all attributes need to be provided


if TYPE_CHECKING:

    class TargetRaterDeleteCommandOptions:
        rater: models.TargetRater


class TargetRaterDeleteCommand(
    CommonSlashCommand["TargetRaterDeleteCommandOptions"],
    name="delete",
    description="Delete a target rater.",
    parent=TargetRaterCommand,
    options=[options.TARGET_RATER],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetRaterEditCommandOptions:
        cities: quarrel.Missing[models.Condition]
        infrastructure: quarrel.Missing[models.Condition]
        activity: quarrel.Missing[models.Condition]
        soldiers: quarrel.Missing[models.Condition]
        tanks: quarrel.Missing[models.Condition]
        aircraft: quarrel.Missing[models.Condition]
        ships: quarrel.Missing[models.Condition]
        missiles: quarrel.Missing[models.Condition]
        nukes: quarrel.Missing[models.Condition]
        money: quarrel.Missing[models.Condition]
        coal: quarrel.Missing[models.Condition]
        oil: quarrel.Missing[models.Condition]
        uranium: quarrel.Missing[models.Condition]
        iron: quarrel.Missing[models.Condition]
        bauxite: quarrel.Missing[models.Condition]
        lead: quarrel.Missing[models.Condition]
        gasoline: quarrel.Missing[models.Condition]
        munitions: quarrel.Missing[models.Condition]
        steel: quarrel.Missing[models.Condition]
        aluminum: quarrel.Missing[models.Condition]
        food: quarrel.Missing[models.Condition]


class TargetRaterEditCommand(
    CommonSlashCommand["TargetRaterEditCommandOptions"],
    name="edit",
    description="Edit a target rater.",
    parent=TargetRaterCommand,
    options=[*options.TARGET_RATER_ATTRIBUTES],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetRaterListCommandOptions:
        user: quarrel.User | quarrel.Member


class TargetRaterListCommand(
    CommonSlashCommand["TargetRaterListCommandOptions"],
    name="list",
    description="List your target raters.",
    parent=TargetRaterCommand,
    options=[options.USER_OPTIONAL],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
