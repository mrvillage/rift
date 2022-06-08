# pyright: reportUnusedImport=false

from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, checks, embeds, models, options, utils
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()


if TYPE_CHECKING:
    from typing import Optional

    from quarrel import Missing

    from .. import enums

    class TicketCommandOptions:
        ...


@bot.command
class TicketCommand(
    CommonSlashCommand["TicketCommandOptions"],
    name="ticket",
    description="Manage tickets.",
    checks=[checks.guild_only],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TicketConfigCommandOptions:
        ...


class TicketConfigCommand(
    CommonSlashCommand["TicketConfigCommandOptions"],
    name="config",
    description="Manage ticket configs.",
    parent=TicketCommand,
    checks=[checks.has_discord_role_permissions(manage_guild=True)],
):
    __slots__ = ()

    async def callback(self) -> None:
        ...


if TYPE_CHECKING:

    class TicketConfigInfoCommandOptions:
        config: models.TicketConfig


class TicketConfigInfoCommand(
    CommonSlashCommand["TicketConfigInfoCommandOptions"],
    name="info",
    description="View information about a ticket config.",
    parent=TicketConfigCommand,
    options=[options.TICKET_CONFIG],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_message(
            embed=self.options.config.build_embed(self.interaction),
        )


if TYPE_CHECKING:

    class TicketConfigCreateCommandOptions:
        name: str
        category: quarrel.CategoryChannel
        archive_category: Optional[quarrel.CategoryChannel]
        default: bool
        name_format: str
        close_action: enums.TicketCloseAction


class TicketConfigCreateCommand(
    CommonSlashCommand["TicketConfigCreateCommandOptions"],
    name="create",
    description="Create a ticket config.",
    parent=TicketConfigCommand,
    options=[
        options.NAME,
        options.CATEGORY,
        options.ARCHIVE_CATEGORY_DEFAULT_NONE,
        options.DEFAULT_BOOL,
        options.NAME_FORMAT,
        options.CLOSE_ACTION,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        if TYPE_CHECKING:
            assert self.interaction.guild is not None
        config = await models.TicketConfig.create(
            name=self.options.name,
            category=self.options.category,
            guild=self.interaction.guild,
            archive_category=self.options.archive_category,
            default=self.options.default,
            name_format=self.options.name_format,
            close_action=self.options.close_action,
        )
        await self.interaction.respond_with_message(
            embed=embeds.ticket_config_created(self.interaction, config),
            grid=config.build_edit_message_grid(),
        )


if TYPE_CHECKING:

    class TicketConfigDeleteCommandOptions:
        config: models.TicketConfig


class TicketConfigDeleteCommand(
    CommonSlashCommand["TicketConfigDeleteCommandOptions"],
    name="delete",
    description="Delete a ticket config.",
    parent=TicketConfigCommand,
    options=[options.TICKET_CONFIG],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.config.delete()
        await self.interaction.respond_with_message(
            embed=embeds.ticket_config_deleted(self.interaction, self.options.config),
        )


if TYPE_CHECKING:

    class TicketConfigEditCommandOptions:
        config: models.TicketConfig
        name: Missing[str]
        category: Missing[quarrel.CategoryChannel]
        archive_category: Missing[Optional[quarrel.CategoryChannel]]
        default: Missing[bool]
        name_format: Missing[str]
        close_action: Missing[enums.TicketCloseAction]


class TicketConfigEditCommand(
    CommonSlashCommand["TicketConfigEditCommandOptions"],
    name="edit",
    description="Edit a ticket config.",
    parent=TicketConfigCommand,
    options=[
        options.TICKET_CONFIG,
        options.NAME_OPTIONAL,
        options.CATEGORY_OPTIONAL,
        options.ARCHIVE_CATEGORY_OPTIONAL,
        options.DEFAULT_BOOL_OPTIONAL,
        options.NAME_FORMAT_OPTIONAL,
        options.CLOSE_ACTION_OPTIONAL,
    ],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.config.edit(
            name=self.options.name,
            category=self.options.category,
            archive_category=self.options.archive_category,
            default=self.options.default,
            name_format=self.options.name_format,
            close_action=self.options.close_action,
        )
        await self.interaction.respond_with_message(
            embed=embeds.ticket_config_edited(self.interaction, self.options.config),
            grid=self.options.config.build_edit_message_grid(),
        )


if TYPE_CHECKING:

    class TicketConfigListCommandOptions:
        ...


class TicketConfigListCommand(
    CommonSlashCommand["TicketConfigListCommandOptions"],
    name="list",
    description="List your ticket configs.",
    parent=TicketConfigCommand,
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond_with_message(
            embed=embeds.ticket_config_list(
                self.interaction,
                utils.sort_models_by_id(
                    cache.ticket_configs,
                    lambda x: x.guild_id == self.interaction.guild_id,
                ),
            ),
        )


if TYPE_CHECKING:

    class TicketOpenCommandOptions:
        config: models.TicketConfig


class TicketOpenCommand(
    CommonSlashCommand["TicketOpenCommandOptions"],
    name="open",
    description="Open a ticket.",
    parent=TicketCommand,
    options=[options.TICKET_CONFIG_DEFAULT_DEFAULT],
):
    __slots__ = ()

    async def callback(self) -> None:
        if TYPE_CHECKING:
            assert isinstance(self.interaction.user, quarrel.Member)
        ticket = await self.options.config.open_ticket(self.interaction.user)
        await self.interaction.respond_with_message(
            embed=embeds.ticket_opened(self.interaction, ticket),
            ephemeral=True,
        )


if TYPE_CHECKING:

    class TicketCloseCommandOptions:
        ticket: models.Ticket


class TicketCloseCommand(
    CommonSlashCommand["TicketCloseCommandOptions"],
    name="close",
    description="Close a ticket.",
    parent=TicketCommand,
    options=[options.TICKET_DEFAULT_CURRENT],
    checks=[checks.own_ticket_or_has_permissions],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.options.ticket.close()
        await self.interaction.respond_with_message(
            embed=embeds.ticket_closed(self.interaction, self.options.ticket),
            ephemeral=True,
        )
