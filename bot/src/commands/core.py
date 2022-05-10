from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import models, options
from ..bot import bot
from .common import CommonSlashCommand

__all__ = ()

if TYPE_CHECKING:

    class NationCommandOptions:
        nation: models.Nation
        user: models.User


@bot.command
class NationCommand(
    CommonSlashCommand["NationCommandOptions"],
    name="nation",
    description="View a nation's information.",
    options=[options.NATION_DEFAULT_SELF, options.USER_OPTIONAL],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond(
            quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            embed=self.options.nation.build_embed(self.interaction.user),
        )


if TYPE_CHECKING:

    class AllianceCommandOptions:
        alliance: models.Alliance
        user: models.User


@bot.command
class AllianceCommand(
    CommonSlashCommand["AllianceCommandOptions"],
    name="alliance",
    description="View an alliance's information.",
    options=[options.ALLIANCE_DEFAULT_SELF, options.USER_OPTIONAL],
):
    __slots__ = ()

    async def callback(self) -> None:
        await self.interaction.respond(
            quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            content=self.options.alliance.name,
        )
