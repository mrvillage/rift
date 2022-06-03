from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import cache, utils
from ...bot import bot

__all__ = ("MenuInterface",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    import quarrel

    from ... import models


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class MenuInterface:
    TABLE: ClassVar[str] = "menu_interfaces"
    id: int
    menu_id: int
    message_id: int
    channel_id: int
    guild_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MenuInterface:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: MenuInterface) -> MenuInterface:
        ...

    @classmethod
    async def create(cls, menu: models.Menu, message: quarrel.Message) -> MenuInterface:
        if message.channel is not quarrel.MISSING:
            guild_id = getattr(message.channel, "guild_id", quarrel.MISSING) or 0
        else:
            guild_id = 0
        self = cls(
            id=0,
            menu_id=menu.id,
            message_id=message.id,
            channel_id=message.channel_id,
            guild_id=guild_id,
        )
        await self.save()
        cache.add_menu_interface(self)
        return self

    @property
    def guild(self) -> Optional[quarrel.Guild]:
        return bot.get_guild(self.guild_id)

    @property
    def menu(self) -> Optional[models.Menu]:
        return cache.get_menu(self.menu_id)

    async def update_interface(self) -> None:
        menu = self.menu
        guild = self.guild
        if menu is None or guild is None:
            return
        await bot.edit_message(
            self.channel_id,
            self.message_id,
            embed=menu.build_interface_embed(guild),
            grid=menu.build_interface_grid(),
        )
