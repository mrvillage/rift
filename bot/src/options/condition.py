from __future__ import annotations

import quarrel

from .. import models
from .common import CommonOption

__all__ = (
    "CONDITION",
    "CONDITION_OPTIONAL",
)

CONDITION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="condition",
    description="The condition to use.",
    converter=models.Condition.convert,
)
CONDITION_OPTIONAL = CONDITION(default=quarrel.MISSING)
