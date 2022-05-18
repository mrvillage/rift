from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, checks, embeds, errors, models, utils
from ..bot import bot
from .common import CommonButton, CommonGrid

__all__ = ("MenuLayoutGrid", "MenuCreateModal", "MenuEditModal")

if TYPE_CHECKING:
    from quarrel import Missing


class MenuLayoutGrid(CommonGrid):
    def __init__(self, menu: models.Menu) -> None:
        super().__init__(timeout=None)
        self.menu: models.Menu = menu
        for row, i in enumerate(menu.layout):
            for column, id in enumerate(i):
                item = cache.get_menu_item(id)
                if item is None:
                    continue
                self.add_component(
                    MenuLayoutButton(item, row=row + 1, column=column + 1)
                )


@bot.component
class MenuLayoutButton(CommonButton):
    def __init__(
        self,
        item: Missing[models.MenuItem] = quarrel.MISSING,
        row: Missing[int] = quarrel.MISSING,
        column: Missing[int] = quarrel.MISSING,
    ) -> None:
        super().__init__(
            custom_id=f"info-menu-item-{item.id}-{row or 0}-{column or 0}"
            if item
            else quarrel.MISSING,
            label=item.id if item else quarrel.MISSING,
            style=quarrel.ButtonStyle.GRAY,
            pattern="info-menu-item-(?P<item_id>[0-9]+)-(?P<row>[0-9]+)-(?P<column>[0-9]+)",
            row=row,
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]
    ) -> None:
        if groups is quarrel.MISSING:
            return
        try:
            item_id = utils.convert_int(groups["item_id"])
        except ValueError:
            return
        item = cache.get_menu_item(item_id)
        if item is None:
            raise errors.MenuItemNotFoundError(interaction, item_id)
        await interaction.respond_with_message(
            embed=item.build_embed(interaction),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class MenuCreateModalComponents(quarrel.ModalValues):
        name: quarrel.TextInputValue
        description: quarrel.TextInputValue


@bot.modal
class MenuCreateModal(
    quarrel.Modal["MenuCreateModalComponents"],
    checks=[
        checks.modal_guild_only,
        checks.modal_has_guild_role_permissions(manage_menus=True),
    ],
):
    def __init__(self) -> None:
        super().__init__(
            title="Create Menu",
            custom_id="modal-menu-create",
            pattern="modal-menu-create",
        )
        self.add_component(
            quarrel.TextInput(
                "name",
                style=quarrel.TextInputStyle.SHORT,
                label="Name",
                required=True,
                max_length=50,
            ),
        )
        self.add_component(
            quarrel.TextInput(
                "description",
                style=quarrel.TextInputStyle.PARAGRAPH,
                label="Description",
                required=True,
                max_length=1000,
            )
        )

    async def callback(
        self,
        interaction: quarrel.Interaction,
        groups: Missing[dict[str, str]],
        values: MenuCreateModalComponents,
    ) -> None:
        if TYPE_CHECKING:
            assert interaction.guild_id is not quarrel.MISSING
        menu = await models.Menu.create(
            interaction.guild_id, values.name.value, values.description.value
        )
        await interaction.respond_with_message(
            embed=embeds.menu_created(interaction, menu),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class MenuEditModalComponents(quarrel.ModalValues):
        name: quarrel.TextInputValue
        description: quarrel.TextInputValue


@bot.modal
class MenuEditModal(
    quarrel.Modal["MenuEditModalComponents"],
    checks=[
        checks.modal_guild_only,
        checks.modal_has_guild_role_permissions(manage_menus=True),
    ],
):
    def __init__(self, menu: Missing[models.Menu] = quarrel.MISSING) -> None:
        super().__init__(
            title="Create Menu",
            custom_id=f"modal-menu-{menu.id}-edit" if menu else quarrel.MISSING,
            pattern="modal-menu-(?P<menu_id>[0-9]+)-edit",
        )
        self.add_component(
            quarrel.TextInput(
                "name",
                style=quarrel.TextInputStyle.SHORT,
                label="Name",
                required=True,
                value=menu.name if menu else quarrel.MISSING,
                max_length=50,
            ),
        )
        self.add_component(
            quarrel.TextInput(
                "description",
                style=quarrel.TextInputStyle.PARAGRAPH,
                label="Description",
                required=True,
                value=menu.description if menu else quarrel.MISSING,
                max_length=1000,
            )
        )

    async def callback(
        self,
        interaction: quarrel.Interaction,
        groups: Missing[dict[str, str]],
        values: MenuEditModalComponents,
    ) -> None:
        if TYPE_CHECKING:
            assert interaction.guild_id is not quarrel.MISSING
        if groups is quarrel.MISSING:
            return
        try:
            menu_id = utils.convert_int(groups["menu_id"])
        except ValueError:
            return
        menu = cache.get_menu(menu_id)
        if menu is None:
            raise errors.MenuNotFoundError(interaction, menu_id)
        await menu.edit(values.name.value, values.description.value)
        await interaction.respond_with_message(
            embed=embeds.menu_edited(interaction, menu),
            ephemeral=True,
        )
