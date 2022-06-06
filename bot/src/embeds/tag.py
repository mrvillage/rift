from __future__ import annotations

import quarrel

from .. import consts, models, strings, utils

__all__ = (
    "tag",
    "tag_deleted",
    "tag_created",
    "tag_edited",
    "tag_list",
    "tag_display",
)


def tag(
    interaction: quarrel.Interaction,
    tag: models.Tag,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=tag.text,
        fields=[
            utils.embed_field("ID", tag.id),
            utils.embed_field("Name", tag.name),
            utils.embed_field("Owner", strings.user_mention_id(tag.owner_id)),
            utils.embed_field(
                "Use condition", f"```ts\n{tag.use_condition}```", inline=False
            ),
        ],
        color=consts.INFO_EMBED_COLOR,
    )


def tag_deleted(
    interaction: quarrel.Interaction,
    tag: models.Tag,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.tag_deleted(tag),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def tag_created(
    interaction: quarrel.Interaction,
    tag: models.Tag,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.tag_created(tag),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def tag_edited(
    interaction: quarrel.Interaction,
    tag: models.Tag,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.tag_edited(tag),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def tag_list(
    interaction: quarrel.Interaction,
    tags: list[models.Tag],
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.tag_list(tags),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def tag_display(
    interaction: quarrel.Interaction,
    tag: models.Tag,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.tag_display(tag),
        footer_text=strings.USER_PROVIDED_CONTENT_DISCLAIMER,
        color=consts.SUCCESS_EMBED_COLOR,
    )
