from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import quarrel

from .. import cache, consts, enums, errors, utils
from ..bot import bot

__all__ = ("Ticket",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    from .. import models
    from ..commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Ticket:
    TABLE: ClassVar[str] = "tickets"
    id: int
    ticket_number: int
    config_id: int
    guild_id: int
    channel_id: int
    owner_id: int
    closed: bool

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Ticket:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Ticket) -> Ticket:
        ...

    async def close(self) -> None:
        self.closed = True
        await self.save()
        channel = self.channel
        if channel is None:
            return
        config = self.config
        if config is None:
            return
        if config.close_action is enums.TicketCloseAction.ARCHIVE:
            await channel.edit(
                name=f"archived-{channel.name}"[: consts.MAX_CHANNEL_NAME_LENGTH],
                # not type narrowed
                parent=channel.guild.get_channel(config.archive_category_id) or quarrel.MISSING,  # type: ignore
            )
        elif config.close_action is enums.TicketCloseAction.DELETE:
            await channel.delete()

    @property
    def channel(self) -> Optional[quarrel.TextChannel]:
        guild = self.guild
        if guild is None:
            return
        # not type narrowed
        return guild.get_channel(self.channel_id)  # type: ignore

    @property
    def config(self) -> Optional[models.TicketConfig]:
        return cache.get_ticket_config(self.config_id)

    @classmethod
    async def convert(
        cls, command: CommonSlashCommand[Any], value: quarrel.TextChannel
    ) -> Ticket:
        try:
            return next(i for i in cache.tickets if i.channel_id == value.id)
        except StopIteration as e:
            raise errors.TicketNotFoundError(command.interaction, value.id) from e

    @classmethod
    async def create(
        cls,
        ticket_number: int,
        config: models.TicketConfig,
        guild: quarrel.Guild,
        channel: quarrel.GuildChannel,
        owner: quarrel.Member,
    ) -> Ticket:
        self = cls(
            id=0,
            ticket_number=ticket_number,
            config_id=config.id,
            guild_id=guild.id,
            channel_id=channel.id,
            owner_id=owner.id,
            closed=False,
        )
        await self.save(insert=True)
        cache.add_ticket(self)
        return self

    @property
    def guild(self) -> Optional[quarrel.Guild]:
        return bot.get_guild(self.guild_id)

    @property
    def mention(self) -> str:
        return f"<#{self.channel_id}>"

    @classmethod
    async def open(cls, config: models.TicketConfig, owner: quarrel.Member) -> Ticket:
        try:
            ticket_number = (
                max(
                    (i for i in cache.tickets if i.config_id == config.id),
                    key=lambda i: i.ticket_number,
                ).ticket_number
                + 1
            )
        except ValueError:
            ticket_number = 1
        channel = await owner.guild.create_channel(
            quarrel.ChannelType.GUILD_TEXT,
            config.name_format.format(ticket_number=ticket_number),
            # type not narrowed to CategoryChannel
            parent=owner.guild.get_channel(config.category_id) or quarrel.MISSING,  # type: ignore
        )
        await channel.edit_permission_overwrite(
            quarrel.PermissionOverwrite.from_member(
                owner, allow=quarrel.Permissions(send_messages=True, view_channel=True)
            )
        )
        return await cls.create(
            ticket_number=ticket_number,
            config=config,
            guild=owner.guild,
            channel=channel,
            owner=owner,
        )
