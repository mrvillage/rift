from __future__ import annotations

import quarrel

from .. import models, utils
from .common import CommonOption

__all__ = ("TAG", "TAG_OPTIONAL")

TAG = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="tag",
    description="The tag to use.",
    converter=models.Tag.convert,
)
TAG_OPTIONAL = TAG(default=utils.default_missing)
