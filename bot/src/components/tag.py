from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, checks, embeds, errors, models, utils
from ..bot import bot

__all__ = ("TagCreateModal", "TagEditModal")


if TYPE_CHECKING:
    from quarrel import Missing

    class TagCreateModalComponents(quarrel.ModalValues):
        name: quarrel.TextInputValue
        text: quarrel.TextInputValue
        use_condition: quarrel.TextInputValue


@bot.modal
class TagCreateModal(
    quarrel.Modal["TagCreateModalComponents"],
    checks=[
        checks.modal_guild_only,
        checks.modal_has_guild_role_permissions(manage_menus=True),
    ],
):
    def __init__(self) -> None:
        super().__init__(
            title="Create Tag",
            custom_id="modal-tag-create",
            pattern="modal-tag-create",
        )
        self.add_component(
            quarrel.TextInput(
                "name",
                style=quarrel.TextInputStyle.SHORT,
                label="Name",
                required=True,
                max_length=50,
                custom_id="text-input-tag-create-name",
            ),
        )
        self.add_component(
            quarrel.TextInput(
                "text",
                style=quarrel.TextInputStyle.PARAGRAPH,
                label="Text",
                required=True,
                max_length=4000,
                custom_id="text-input-tag-create-text",
            )
        )
        self.add_component(
            quarrel.TextInput(
                "use-condition",
                style=quarrel.TextInputStyle.PARAGRAPH,
                label="Use Condition",
                required=True,
                max_length=1000,
                attribute="use_condition",
                value="false",
                custom_id="text-input-tag-create-use-condition",
            )
        )

    async def callback(
        self,
        interaction: quarrel.Interaction,
        groups: Missing[dict[str, str]],
        values: TagCreateModalComponents,
    ) -> None:
        tag = await models.Tag.create(
            values.name.value,
            interaction.user.id,
            values.text.value,
            models.Condition.parse_from_interaction(
                interaction, values.use_condition.value
            ),
        )
        await interaction.respond_with_message(
            embed=embeds.tag_created(interaction, tag),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class TagEditModalComponents(quarrel.ModalValues):
        name: quarrel.TextInputValue
        text: quarrel.TextInputValue
        use_condition: quarrel.TextInputValue


@bot.modal
class TagEditModal(
    quarrel.Modal["TagEditModalComponents"],
    checks=[
        checks.modal_guild_only,
        checks.modal_has_guild_role_permissions(manage_menus=True),
    ],
):
    def __init__(self, tag: Missing[models.Tag] = quarrel.MISSING) -> None:
        super().__init__(
            title="Edit Tag",
            custom_id=f"modal-tag-{tag.id}-edit" if tag else quarrel.MISSING,
            pattern="modal-tag-(?P<id>[0-9]+)-edit",
        )
        self.add_component(
            quarrel.TextInput(
                "name",
                style=quarrel.TextInputStyle.SHORT,
                label="Name",
                required=True,
                value=tag.name if tag else quarrel.MISSING,
                max_length=50,
                custom_id="text-input-tag-edit-name",
            ),
        )
        self.add_component(
            quarrel.TextInput(
                "text",
                style=quarrel.TextInputStyle.PARAGRAPH,
                label="Text",
                required=True,
                value=tag.text if tag else quarrel.MISSING,
                max_length=4000,
                custom_id="text-input-tag-edit-text",
            )
        )
        self.add_component(
            quarrel.TextInput(
                "use-condition",
                style=quarrel.TextInputStyle.PARAGRAPH,
                label="Use Condition",
                required=True,
                value=tag.use_condition if tag else quarrel.MISSING,
                max_length=1000,
                attribute="use_condition",
                custom_id="text-input-tag-edit-use-condition",
            )
        )

    async def callback(
        self,
        interaction: quarrel.Interaction,
        groups: Missing[dict[str, str]],
        values: TagEditModalComponents,
    ) -> None:
        if (
            tag := utils.regex_groups_to_model(
                interaction, groups, cache.get_tag, errors.TagNotFoundError
            )
        ) is None:
            return
        await tag.edit(
            values.name.value,
            values.text.value,
            models.Condition.parse_from_interaction(
                interaction, values.use_condition.value
            ),
        )
        await interaction.respond_with_message(
            embed=embeds.tag_edited(interaction, tag),
            ephemeral=True,
        )
