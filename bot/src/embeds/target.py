from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import consts, strings, utils

__all__ = ("targets", "target_find_wizard", "target_find_processing")

if TYPE_CHECKING:
    from .. import models


def targets(
    interaction: quarrel.Interaction,
    targets: list[models.Target],
    page: int,
    nation: models.Nation,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        color=consts.INFO_EMBED_COLOR,
        description=strings.targets(targets, page, nation),
        fields=[
            i.build_embed_field()
            for i in targets[
                (page - 1) * consts.TARGETS_PER_PAGE : page * consts.TARGETS_PER_PAGE
            ]
        ],
    )


def target_find_wizard(interaction: quarrel.Interaction) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        color=consts.INFO_EMBED_COLOR,
        description=strings.target_find_wizard(),
    )


def target_find_processing(interaction: quarrel.Interaction) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        color=consts.PENDING_EMBED_COLOR,
        description=strings.TARGET_FIND_PROCESSING,
    )
