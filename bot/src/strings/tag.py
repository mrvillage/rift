from __future__ import annotations

from typing import TYPE_CHECKING

from .. import strings

__all__ = (
    "tag_deleted",
    "tag_created",
    "tag_edited",
    "tag_list",
    "tag_display",
)

if TYPE_CHECKING:
    from .. import models


def tag_deleted(tag: models.Tag) -> str:
    return strings.model_deleted("Tag", tag)


def tag_created(tag: models.Tag) -> str:
    return strings.model_created("Tag", tag)


def tag_edited(tag: models.Tag) -> str:
    return strings.model_edited("Tag", tag)


def tag_list(tag: list[models.Tag]) -> str:
    return strings.model_list("Tag", tag)


def tag_display(tag: models.Tag) -> str:
    return f"{tag.text}\n\n*Created by {strings.user_mention_id(tag.owner_id)}*"
