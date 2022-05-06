from __future__ import annotations

import quarrel

from .. import models, utils
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
NATION_DEFAULT_SELF = NATION(default=utils.self_nation)
ALLIANCE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="alliance",
    description="The alliance to use.",
    converter=models.Alliance.convert,
)
ALLIANCE_DEFAULT_SELF = ALLIANCE(default=utils.self_alliance)
