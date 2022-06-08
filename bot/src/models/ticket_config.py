from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import cache, components, embeds, enums, errors, models, utils

__all__ = ("TicketConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    import quarrel
    from quarrel import Missing

    from ..commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TicketConfig:
    TABLE: ClassVar[str] = "ticket_configs"
    id: int
    name: str
    category_id: int
    guild_id: int
    message: str
    archive_category_id: Optional[int]
    mention_ids: list[int]
    default: bool
    name_format: str
    interview_config_id: Optional[int]
    close_action: enums.TicketCloseAction
    transcript_channel_id: Optional[int]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TicketConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: TicketConfig) -> TicketConfig:
        ...

    # TODO: implement
    def build_edit_message_grid(self) -> quarrel.Grid:
        return components.TicketConfigEditMessageGrid(self)

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.ticket_config(interaction, self)

    @classmethod
    async def convert(
        cls, command: CommonSlashCommand[Any], value: str
    ) -> TicketConfig:
        return utils.convert_model(
            enums.ConvertType.STR_EQ,
            command.interaction,
            value,
            cache.get_ticket_config,
            {
                i
                for i in cache.ticket_configs
                if i.guild_id == command.interaction.guild_id
            },
            "name",
            errors.TicketConfigNotFoundError,
        )

    @classmethod
    async def create(
        cls,
        name: str,
        category: quarrel.CategoryChannel,
        guild: quarrel.Guild,
        archive_category: Optional[quarrel.CategoryChannel],
        default: bool,
        name_format: str,
        close_action: enums.TicketCloseAction,
    ) -> TicketConfig:
        self = cls(
            id=0,
            name=name,
            category_id=category.id,
            guild_id=guild.id,
            message="Welcome to your ticket!",
            archive_category_id=archive_category.id
            if archive_category is not None
            else None,
            mention_ids=[],
            default=default,
            name_format=name_format,
            interview_config_id=0,
            close_action=close_action,
            transcript_channel_id=None,
        )
        await self.save(insert=True)
        cache.add_ticket_config(self)
        return self

    async def edit(
        self,
        name: Missing[str],
        category: Missing[quarrel.CategoryChannel],
        archive_category: Missing[Optional[quarrel.CategoryChannel]],
        default: Missing[bool],
        name_format: Missing[str],
        close_action: Missing[enums.TicketCloseAction],
    ) -> None:
        if name is not quarrel.MISSING:
            self.name = name
        if category is not quarrel.MISSING:
            self.category_id = category.id
        if archive_category is not quarrel.MISSING:
            self.archive_category_id = archive_category and archive_category.id
        if default is not quarrel.MISSING:
            self.default = default
        if name_format is not quarrel.MISSING:
            self.name_format = name_format
        if close_action is not quarrel.MISSING:
            self.close_action = close_action
        await self.save()

    async def open_ticket(self, user: quarrel.Member) -> models.Ticket:
        return await models.Ticket.open(self, user)
