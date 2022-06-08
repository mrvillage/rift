from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, checks, embeds, errors, models, utils
from ..bot import bot
from .common import CommonButton, CommonGrid

__all__ = (
    "TicketConfigEditMessageGrid",
    "TicketConfigEditMessageModal",
)


class TicketConfigEditMessageGrid(CommonGrid):
    def __init__(self, config: models.TicketConfig) -> None:
        super().__init__(timeout=None)
        self.config: models.TicketConfig = config
        self.add_component(TicketConfigEditMessageButton(config))


@bot.component
class TicketConfigEditMessageButton(CommonButton):
    def __init__(self, config: Missing[models.TicketConfig] = quarrel.MISSING) -> None:
        super().__init__(
            custom_id=f"ticket-config-{config.id}-edit-message"
            if config
            else quarrel.MISSING,
            label="Edit Message",
            style=quarrel.ButtonStyle.GRAY,
            pattern="ticket-config-(?P<id>[0-9]+)-edit-message",
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]
    ) -> None:
        if (
            config := utils.regex_groups_to_model(
                interaction,
                groups,
                cache.get_ticket_config,
                errors.TicketConfigNotFoundError,
            )
        ) is None:
            return
        await interaction.respond_with_modal(
            modal=TicketConfigEditMessageModal(config),
        )


if TYPE_CHECKING:
    from quarrel import Missing

    class TicketConfigEditMessageModalComponents(quarrel.ModalValues):
        message: quarrel.TextInputValue


@bot.modal
class TicketConfigEditMessageModal(
    quarrel.Modal["TicketConfigEditMessageModalComponents"],
    checks=[
        checks.modal_guild_only,
        checks.modal_has_discord_role_permissions(manage_guild=True),
    ],
):
    def __init__(self, config: Missing[models.TicketConfig] = quarrel.MISSING) -> None:
        super().__init__(
            title="Edit Ticket Config",
            custom_id=f"modal-ticket-config-{config.id}-edit-message"
            if config
            else quarrel.MISSING,
            pattern="modal-ticket-config-(?P<id>[0-9]+)-edit-message",
        )
        self.add_component(
            quarrel.TextInput(
                "message",
                style=quarrel.TextInputStyle.SHORT,
                label="Message",
                required=True,
                value=config.name if config else quarrel.MISSING,
                max_length=50,
                custom_id="text-input-ticket-config-edit-message",
            ),
        )

    async def callback(
        self,
        interaction: quarrel.Interaction,
        groups: Missing[dict[str, str]],
        values: TicketConfigEditMessageModalComponents,
    ) -> None:
        if (
            config := utils.regex_groups_to_model(
                interaction,
                groups,
                cache.get_ticket_config,
                errors.TicketConfigNotFoundError,
            )
        ) is None:
            return
        config.message = values.message.value
        await config.save()
        await interaction.respond_with_message(
            embed=embeds.ticket_config_edited(interaction, config),
            ephemeral=True,
        )
