from __future__ import annotations

from typing import TYPE_CHECKING

from .. import embeds
from .base import RiftError

__all__ = ("MenuHasNoSpaceError", "MenuItemHasNoMenuError")

if TYPE_CHECKING:
    import quarrel
    from quarrel import Missing

    from .. import models


class MenuHasNoSpaceError(RiftError):
    def __init__(
        self,
        menu: models.Menu,
        item: models.MenuItem,
        row: Missing[int],
        column: Missing[int],
    ) -> None:
        self.menu: models.Menu = menu
        self.item: models.MenuItem = item
        self.row: Missing[int] = row
        self.column: Missing[int] = column

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.menu_has_no_space_error(
            interaction, self.menu, self.item, self.row, self.column
        )


class MenuItemHasNoMenuError(RiftError):
    def __init__(self, item: models.MenuItem) -> None:
        self.item: models.MenuItem = item

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.menu_item_has_no_menu_error(interaction, self.item)
