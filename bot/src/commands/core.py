from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, embeds, errors, models, options, utils
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
        await self.interaction.respond_with_message(
            embed=self.options.nation.build_embed(self.interaction.user),
            grid=self.options.nation.build_grid(),
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
        await self.interaction.respond_with_message(
            embed=self.options.alliance.build_embed(self.interaction.user),
        )


if TYPE_CHECKING:

    class LinkCommandOptions:
        nation: models.Nation
        user: quarrel.User


@bot.command
class LinkCommand(
    CommonSlashCommand["LinkCommandOptions"],
    name="link",
    description="Link a nation to a Discord account.",
    options=[options.NATION, options.USER_DEFAULT_SELF],
):
    __slots__ = ()

    async def callback(self) -> None:
        user_from_user = cache.get_user(self.options.user.id)
        user_from_nation = cache.get_user(self.options.nation.id)
        if user_from_user is not None and user_from_user.nation_id is not None:
            raise errors.EmbedErrorResponse(
                embed=embeds.user_already_linked(
                    self.interaction.user, self.options.user
                ),
            )
        if user_from_nation is not None:
            raise errors.EmbedErrorResponse(
                embed=embeds.nation_already_linked(
                    self.interaction.user, self.options.nation
                ),
            )
        if (
            await utils.fetch_discord_username(self.options.nation)
            != self.options.user.name
        ):
            raise errors.EmbedErrorResponse(
                embed=embeds.nation_username_mismatch(
                    self.interaction.user, self.options.nation, self.options.user
                ),
            )
        if user_from_user is not None:
            user_from_user.nation_id = self.options.nation.id
            await user_from_user.save()
        else:
            await models.User.link(self.options.user, self.options.nation)
        await self.interaction.respond_with_message(
            embed=embeds.linked_to(
                self.interaction.user, self.options.nation, self.options.user
            ),
            ephemeral=True,
        )



if TYPE_CHECKING:

    class MeCommandOptions:
        ...


@bot.command
class MeCommand(
    CommonSlashCommand["MeCommandOptions"],
    name="me",
    description="View your nation information.",
    options=[],
    checks=[],
):
    __slots__ = ()

    async def callback(self) -> None:
        user = cache.get_user(self.interaction.user.id)
        if user is None or (nation := user.nation) is None:
            raise errors.NationNotFoundError(self.interaction)
        await self.interaction.respond_with_message(
            embed=nation.build_embed(self.interaction.user),
            grid=nation.build_grid(),
        )
