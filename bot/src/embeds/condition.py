from __future__ import annotations

from typing import TYPE_CHECKING

from .. import consts, strings, utils

__all__ = (
    "condition",
    "condition_list",
    "condition_deleted",
    "condition_created",
    "condition_edited",
)

if TYPE_CHECKING:
    import quarrel

    from .. import models


def condition(
    interaction: quarrel.Interaction, condition: models.Condition
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        fields=[
            utils.embed_field("ID", condition.id),
            utils.embed_field("Name", condition.name),
            utils.embed_field("Owner", strings.user_mention_id(condition.owner_id)),
            utils.embed_field("Public", condition.public),
            utils.embed_field("Use condition", condition.use_condition),
            utils.embed_field("Condition", condition.value),
        ],
    )


def condition_list(
    interaction: quarrel.Interaction, conditions: list[models.Condition]
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.condition_list(conditions),
        color=consts.INFO_EMBED_COLOR,
    )


def condition_deleted(
    interaction: quarrel.Interaction, condition: models.Condition
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.condition_deleted(condition),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def condition_created(
    interaction: quarrel.Interaction, condition: models.Condition
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.condition_created(condition),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def condition_edited(
    interaction: quarrel.Interaction, condition: models.Condition
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.condition_edited(condition),
        color=consts.SUCCESS_EMBED_COLOR,
    )
