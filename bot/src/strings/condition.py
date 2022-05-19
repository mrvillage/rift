from __future__ import annotations

from typing import TYPE_CHECKING

from .. import strings

__all__ = (
    "condition_deleted",
    "condition_created",
    "condition_edited",
    "condition_list",
)

if TYPE_CHECKING:

    from .. import models


def condition_deleted(condition: models.Condition) -> str:
    return strings.model_deleted("Condition", condition)


def condition_created(condition: models.Condition) -> str:
    return strings.model_created("Condition", condition)


def condition_edited(condition: models.Condition) -> str:
    return strings.model_edited("Condition", condition)


def condition_list(conditions: list[models.Condition]) -> str:
    return strings.model_list("Condition", conditions)
