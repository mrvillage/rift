from __future__ import annotations

from typing import TYPE_CHECKING

from .. import consts, strings, utils

__all__ = (
    "menu_has_no_space_error",
    "menu_item_created",
    "menu_item_deleted",
    "menu_item_edited",
    "menu_item",
    "menu_item_has_no_menu_error",
    "menu_item_moved",
)

if TYPE_CHECKING:
    import quarrel
    from quarrel import Missing

    from .. import models


def menu_has_no_space_error(
    interaction: quarrel.Interaction,
    menu: models.Menu,
    item: models.MenuItem,
    row: Missing[int],
    column: Missing[int],
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_has_no_space(menu, item, row, column),
        color=consts.ERROR_EMBED_COLOR,
    )


def menu_item_created(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_created(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item_deleted(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_deleted(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item_edited(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_edited(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item(interaction: quarrel.Interaction, item: models.MenuItem) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        fields=[
            quarrel.EmbedField(name="ID", value=item.id),
            quarrel.EmbedField(name="Menu ID", value=item.menu_id),
            quarrel.EmbedField(name="Type", value=strings.enum_name(item.type)),
            quarrel.EmbedField(name="Style", value=strings.enum_name(item.style)),
            quarrel.EmbedField(name="Label", value=item.label),
            quarrel.EmbedField(name="Disabled", value=item.disabled),
            quarrel.EmbedField(name="URL", value=item.url),
            quarrel.EmbedField(name="Emoji", value=item.emoji),
            quarrel.EmbedField(
                name="Action",
                value=strings.enum_name(item.action) if item.action else None,
            ),
            quarrel.EmbedField(
                name="Action Options",
                value=", ".join([str(i) for i in item.action_options]),
            ),
        ],
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item_has_no_menu_error(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_has_no_menu(item),
        color=consts.ERROR_EMBED_COLOR,
    )


def menu_item_moved(
    interaction: quarrel.Interaction,
    item: models.MenuItem,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_moved(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )
