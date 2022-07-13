from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from .. import consts, enums, strings, utils

__all__ = (
    "target_field_name",
    "target_field_value",
    "targets",
    "target_find_wizard",
    "TARGET_FIND_PROCESSING",
)

if TYPE_CHECKING:
    from typing import Final

    from .. import models


def target_field_name(nation: models.Nation, rating: float) -> str:
    return f"{nation} - {rating:,.2f}"


def target_field_value(target: models.Target) -> str:
    return "\n".join(
        f"{attr.name.replace('_', ' ').capitalize()}: {attr.value} - {attr.rating:,.2f}"
        for attr in target.attributes
    )


def targets(targets: list[models.Target], page: int, nation: models.Nation) -> str:
    num_targets = len(targets)
    return f"Showing #{(page-1) * consts.TARGETS_PER_PAGE} to #{min(page*consts.TARGETS_PER_PAGE, num_targets)} of {num_targets:,} targets found for {nation}.\nNote: Resources are an **ESTIMATE**, there is no way to have a 100% accurate estimate of resources."


def target_find_wizard() -> str:
    return f"Select the attributes to count towards target rating below.\nThis menu will expire in {strings.datetime_mention(utils.utcnow()+ datetime.timedelta(seconds=consts.TARGET_FIND_TIMEOUT), enums.TimestampStyle.RELATIVE)}"


TARGET_FIND_PROCESSING: Final[str] = "Finding targets..."
