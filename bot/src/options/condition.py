from __future__ import annotations

import quarrel

from .. import models, utils
from .common import CommonOption

__all__ = (
    "CONDITION",
    "CONDITION_OPTIONAL",
    "EXPRESSION",
    "EXPRESSION_OPTIONAL",
    "USE_CONDITION",
    "USE_CONDITION_OPTIONAL",
    "USE_CONDITION_EXPRESSION",
    "USE_CONDITION_EXPRESSION_OPTIONAL",
)

CONDITION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="condition",
    description="The condition to use.",
    converter=models.Condition.convert,
)
CONDITION_OPTIONAL = CONDITION(default=utils.default_missing)
EXPRESSION = CONDITION(
    name="expression",
    description="The expression to use.",
    converter=lambda command, value: models.Condition.convert(command, value, True),
)
EXPRESSION_OPTIONAL = EXPRESSION(default=utils.default_missing)
USE_CONDITION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="use-condition",
    description="The condition to determine who can use this.",
    converter=models.Condition.convert,
)
USE_CONDITION_OPTIONAL = USE_CONDITION(default=utils.default_missing)
USE_CONDITION_EXPRESSION = USE_CONDITION(
    converter=lambda command, value: models.Condition.convert(command, value, True)
)
USE_CONDITION_EXPRESSION_OPTIONAL = USE_CONDITION_EXPRESSION(
    default=utils.default_missing
)
