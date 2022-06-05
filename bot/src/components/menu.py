from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, checks, embeds, enums, errors, models, utils
from ..bot import bot
from .common import CommonButton, CommonGrid, CommonSelectMenu

__all__ = (
    "MenuLayoutGrid",
    "MenuCreateModal",
    "MenuEditModal",
    "MenuInterfaceGrid",
    "MenuInterfaceButton",
    "MenuInterfaceSelectMenu",
)

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
            custom_id=f"button-menu-item-{item.id}-{row or 0}-{column or 0}-info"
            if item
            else quarrel.MISSING,
            label=item.id if item else quarrel.MISSING,
            style=quarrel.ButtonStyle.GRAY,
            pattern="button-menu-item-(?P<id>[0-9]+)-(?P<row>[0-9]+)-(?P<column>[0-9]+)-info",
            row=row,
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]
    ) -> None:
        if (
            item := utils.regex_groups_to_model(
                interaction, groups, cache.get_menu_item, errors.MenuItemNotFoundError
            )
        ) is None:
            return
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
            title="Edit Menu",
            custom_id=f"modal-menu-{menu.id}-edit" if menu else quarrel.MISSING,
            pattern="modal-menu-(?P<id>[0-9]+)-edit",
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
        if (
            menu := utils.regex_groups_to_model(
                interaction, groups, cache.get_menu, errors.MenuNotFoundError
            )
        ) is None:
            return
        await menu.edit(values.name.value, values.description.value)
        await interaction.respond_with_message(
            embed=embeds.menu_edited(interaction, menu),
            ephemeral=True,
        )


class MenuInterfaceGrid(CommonGrid):
    def __init__(self, menu: models.Menu) -> None:
        super().__init__(timeout=None)
        for row in menu.layout:
            for id in row:
                item = cache.get_menu_item(id)
                if item is None:
                    continue
                self.add_component(item.build_component())


@bot.component
class MenuInterfaceButton(CommonButton, checks=[checks.button_guild_only]):
    def __init__(self, item: Missing[models.MenuItem] = quarrel.MISSING) -> None:
        super().__init__(
            custom_id=f"button-menu-item-{item.id}-run" if item else quarrel.MISSING,
            label=item.label if item else quarrel.MISSING,
            style=item.quarrel_style if item else quarrel.MISSING,
            disabled=item.disabled or quarrel.MISSING if item else quarrel.MISSING,
            url=item.url or quarrel.MISSING if item else quarrel.MISSING,
            pattern="button-menu-item-(?P<id>[0-9]+)-run",
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: Missing[dict[str, str]]
    ) -> None:
        if TYPE_CHECKING:
            assert interaction.guild is not None
            assert isinstance(interaction.user, quarrel.Member)
        if (
            item := utils.regex_groups_to_model(
                interaction, groups, cache.get_menu_item, errors.MenuItemNotFoundError
            )
        ) is None:
            return
        if item.action is enums.MenuItemAction.NONE:
            return
        if item.action is enums.MenuItemAction.ADD_ROLES:
            roles = [
                role
                for id in item.action_options
                if (role := interaction.guild.get_role(id)) is not None
            ]
            for i in roles:
                await interaction.user.add_role(i)
            await interaction.respond_with_message(
                embed=embeds.menu_item_action_added_roles(interaction, roles),
                ephemeral=True,
            )
        elif item.action is enums.MenuItemAction.REMOVE_ROLES:
            current_roles = interaction.user.roles
            roles = utils.unique(
                (
                    role
                    for id in item.action_options
                    if (role := interaction.guild.get_role(id)) is not None
                )
            )
            for i in roles:
                await interaction.user.remove_role(i)
            await interaction.respond_with_message(
                embed=embeds.menu_item_action_removed_roles(interaction, roles),
                ephemeral=True,
            )
        elif item.action is enums.MenuItemAction.TOGGLE_ROLES:
            current_roles = interaction.user.roles
            added = [
                role
                for id in item.action_options
                if (role := interaction.guild.get_role(id)) is not None
                and role not in current_roles
            ]
            removed = [
                role
                for id in item.action_options
                if (role := interaction.guild.get_role(id)) is not None
                and role in current_roles
            ]
            for i in added:
                await interaction.user.add_role(i)
            for i in removed:
                await interaction.user.remove_role(i)
            await interaction.respond_with_message(
                embed=embeds.menu_item_action_toggled_roles(
                    interaction, added, removed
                ),
                ephemeral=True,
            )


@bot.component
class MenuInterfaceSelectMenu(CommonSelectMenu):
    def __init__(self, item: Missing[models.MenuItem] = quarrel.MISSING) -> None:
        super().__init__(
            custom_id=f"select-menu-item-{item.id}-run" if item else quarrel.MISSING,
            pattern="select-menu-item-(?P<id>[0-9]+)-run",
        )
