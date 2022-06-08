from __future__ import annotations

import quarrel

from .. import consts, models, strings, utils

__all__ = (
    "ticket_config",
    "ticket_config_deleted",
    "ticket_config_created",
    "ticket_config_edited",
    "ticket_config_list",
    "ticket_opened",
    "ticket_closed",
    "ticket_config_no_default_error",
)


def ticket_config(
    interaction: quarrel.Interaction,
    config: models.TicketConfig,
) -> quarrel.Embed:  # sourcery skip: or-if-exp-identity
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=config.message,
        fields=[
            utils.embed_field("ID", config.id),
            utils.embed_field("Name", config.name),
            utils.embed_field("Default", strings.display_bool(config.default)),
            utils.embed_field(
                "Category",
                strings.category_name_id(interaction.guild_id, config.category_id)
                if interaction.guild_id and config.category_id
                else strings.NONE,
            ),
            utils.embed_field(
                "Archive Category",
                strings.category_name_id(
                    interaction.guild_id, config.archive_category_id
                )
                if interaction.guild_id and config.archive_category_id
                else strings.NONE,
            ),
            utils.embed_field(
                "Name Format",
                config.name_format if config.name_format else strings.NONE,
            ),
            # TODO: Add interview config
            # TODO: Add mention IDs
        ],
        color=consts.INFO_EMBED_COLOR,
    )


def ticket_config_deleted(
    interaction: quarrel.Interaction,
    config: models.TicketConfig,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.ticket_config_deleted(config),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def ticket_config_created(
    interaction: quarrel.Interaction,
    config: models.TicketConfig,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.ticket_config_created(config),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def ticket_config_edited(
    interaction: quarrel.Interaction,
    config: models.TicketConfig,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.ticket_config_edited(config),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def ticket_config_list(
    interaction: quarrel.Interaction,
    configs: list[models.TicketConfig],
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.ticket_config_list(configs),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def ticket_opened(
    interaction: quarrel.Interaction,
    ticket: models.Ticket,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.ticket_opened(ticket),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def ticket_closed(
    interaction: quarrel.Interaction,
    ticket: models.Ticket,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.ticket_closed(ticket),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def ticket_config_no_default_error(interaction: quarrel.Interaction) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.TICKET_CONFIG_NO_DEFAULT_ERROR,
        color=consts.ERROR_EMBED_COLOR,
    )
