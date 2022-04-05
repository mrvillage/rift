from __future__ import annotations

import quarrel

from .. import models, utils
from .common import CommonOption

__all__ = (
    "TARGET_CONFIG",
    "TARGET_CONFIG_OPTIONAL",
    "TARGET_RATER",
    "TARGET_RATER_OPTIONAL",
    "TARGET_RATER_ATTRIBUTES",
    "TARGET_FIND_ATTACK",
    "TARGET_FIND_ATTACK_OPTIONAL",
    "USE_TARGET_CONFIG_CONDITION",
    "BASE_TARGET_RATER",
    "BASE_TARGET_RATER_OPTIONAL",
)

TARGET_CONFIG = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="config",
    description="The target config to use.",
    converter=models.TargetConfig.convert,
)
TARGET_CONFIG_OPTIONAL = TARGET_CONFIG(default=utils.default_missing)
TARGET_RATER = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="rater",
    description="The target rater to use.",
    converter=models.TargetRater.convert,
)
TARGET_RATER_OPTIONAL = TARGET_RATER(default=utils.default_missing)
TARGET_RATER_ATTRIBUTE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="",
    description="",
    converter=models.Condition.convert,
    default=utils.default_missing,
)

TARGET_RATER_ATTRIBUTES = (
    TARGET_RATER_ATTRIBUTE(name="cities", description="The rater for cities."),
    TARGET_RATER_ATTRIBUTE(
        name="infrastructure", description="The rater for infrastructure."
    ),
    TARGET_RATER_ATTRIBUTE(name="activity", description="The rater for activity."),
    TARGET_RATER_ATTRIBUTE(name="soldiers", description="The rater for soldiers."),
    TARGET_RATER_ATTRIBUTE(name="tanks", description="The rater for tanks."),
    TARGET_RATER_ATTRIBUTE(name="aircraft", description="The rater for aircraft."),
    TARGET_RATER_ATTRIBUTE(name="ships", description="The rater for ships."),
    TARGET_RATER_ATTRIBUTE(name="missiles", description="The rater for missiles."),
    TARGET_RATER_ATTRIBUTE(name="nukes", description="The rater for nukes."),
    TARGET_RATER_ATTRIBUTE(name="money", description="The rater for money."),
    TARGET_RATER_ATTRIBUTE(name="coal", description="The rater for coal."),
    TARGET_RATER_ATTRIBUTE(name="oil", description="The rater for oil."),
    TARGET_RATER_ATTRIBUTE(name="uranium", description="The rater for uranium."),
    TARGET_RATER_ATTRIBUTE(name="iron", description="The rater for iron."),
    TARGET_RATER_ATTRIBUTE(name="bauxite", description="The rater for bauxite."),
    TARGET_RATER_ATTRIBUTE(name="lead", description="The rater for lead."),
    TARGET_RATER_ATTRIBUTE(name="gasoline", description="The rater for gasoline."),
    TARGET_RATER_ATTRIBUTE(name="munitions", description="The rater for munitions."),
    TARGET_RATER_ATTRIBUTE(name="steel", description="The rater for steel."),
    TARGET_RATER_ATTRIBUTE(name="aluminum", description="The rater for aluminum."),
    TARGET_RATER_ATTRIBUTE(name="food", description="The rater for food."),
)

TARGET_FIND_ATTACK = CommonOption(
    type=quarrel.ApplicationCommandOptionType.BOOLEAN,
    name="attack",
    description="Find targets to attack the nation instead.",
    default=False,
)
TARGET_FIND_ATTACK_OPTIONAL = TARGET_FIND_ATTACK(default=utils.default_missing)
USE_TARGET_CONFIG_CONDITION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.BOOLEAN,
    name="use-config-condition",
    description="Whether or not to use the target config condition.",
    default=True,
)
BASE_TARGET_RATER = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="base-rater",
    description="The rater to use for unprovided ratings.",
    converter=models.TargetRater.convert,
)
BASE_TARGET_RATER_OPTIONAL = BASE_TARGET_RATER(default=utils.default_missing)
