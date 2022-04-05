from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import models, options
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
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TargetFindCommandOptions:
        config: quarrel.Missing[models.TargetConfig]
        rater: quarrel.Missing[models.TargetRater]
        attack: bool
        condition: quarrel.Missing[models.Condition]
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
        options.TARGET_FIND_ATTACK,
        options.CONDITION_OPTIONAL,
        options.NATION_DEFAULT_SELF,
        options.USE_TARGET_CONFIG_CONDITION,
    ],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...  # if a config isn't provided for the counting, have a follow up with a select menu to determine the "counting"


if TYPE_CHECKING:

    class TargetConfigCommandOptions:
        ...


class TargetConfigCommand(
    CommonSlashCommand["TargetConfigCommandOptions"],
    name="config",
    description="Manage target configs.",
    parent=TargetCommand,
    options=[],
    checks=[],
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
    checks=[],
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
        public: bool


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
        options.PUBLIC_DEFAULT_FALSE,
    ],
    checks=[],
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
    checks=[],
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
        public: quarrel.Missing[bool]


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
        options.PUBLIC_OPTIONAL,
    ],
    checks=[],
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
    checks=[],
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
    options=[],
    checks=[],
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
    checks=[],
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
    checks=[],
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
    checks=[],
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
    checks=[],
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
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...
