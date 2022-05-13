from __future__ import annotations

import quarrel

from .. import models, utils
from .common import CommonOption

__all__ = (
    "NATION",
    "NATION_DEFAULT_SELF",
    "ALLIANCE",
    "ALLIANCE_DEFAULT_SELF",
    "NATION_OR_ALLIANCE",
    "NATION_OR_ALLIANCE_DEFAULT_SELF_NATION",
    "NATION_OR_ALLIANCE_DEFAULT_SELF_ALLIANCE",
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
NATION_OR_ALLIANCE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="search",
    description="The nation or alliance to search for.",
    converter=utils.nation_or_alliance,
)
NATION_OR_ALLIANCE_DEFAULT_SELF_NATION = NATION_OR_ALLIANCE(default=utils.self_nation)
NATION_OR_ALLIANCE_DEFAULT_SELF_ALLIANCE = ALLIANCE(default=utils.self_alliance)
