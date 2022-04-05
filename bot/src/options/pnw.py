from __future__ import annotations

import quarrel

from .. import models
from .common import CommonOption

__all__ = (
    "NATION",
    "NATION_DEFAULT_SELF",
    "ALLIANCE",
    "ALLIANCE_DEFAULT_SELF",
)

NATION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="nation",
    description="The nation to use.",
    converter=models.Nation.convert,
)
NATION_DEFAULT_SELF = NATION(
    converter=lambda command, value: models.Nation.convert(
        command, value, default_to_self=True
    )
)
ALLIANCE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="alliance",
    description="The alliance to use.",
    converter=models.Alliance.convert,
)
ALLIANCE_DEFAULT_SELF = ALLIANCE(
    converter=lambda command, value: models.Alliance.convert(
        command, value, default_to_self=True
    )
)
