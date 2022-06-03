from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import cache, errors, models, utils
from ..bot import bot
from .common import CommonButton, CommonGrid

__all__ = ("NationGrid",)

if TYPE_CHECKING:
    from quarrel import Missing


class NationGrid(CommonGrid):
    def __init__(self, nation: models.Nation) -> None:
        super().__init__(timeout=None)
        self.nation: models.Nation = nation
        self.add_component(NationRefreshButton(nation))
        self.add_component(NationAllianceInformationButton(nation))


@bot.component
class NationRefreshButton(CommonButton):
    def __init__(self, nation: Missing[models.Nation] = quarrel.MISSING) -> None:
        super().__init__(
            custom_id=f"nation-{nation.id}-info-refresh" if nation else quarrel.MISSING,
            label="Refresh",
            style=quarrel.ButtonStyle.GRAY,
            pattern="nation-(?P<id>[0-9]+)-info-refresh",
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]
    ) -> None:
        if (
            nation := utils.regex_groups_to_model(
                interaction, groups, cache.get_nation, errors.NationNotFoundError
            )
        ) is None:
            return
        await interaction.respond_with_edit(
            embed=nation.build_embed(interaction),
        )


@bot.component
class NationAllianceInformationButton(CommonButton):
    def __init__(self, nation: Missing[models.Nation] = quarrel.MISSING) -> None:
        super().__init__(
            custom_id=f"nation-{nation.id}-alliance-info"
            if nation
            else quarrel.MISSING,
            label="Alliance Information",
            style=quarrel.ButtonStyle.GRAY,
            pattern="nation-(?P<id>[0-9]+)-alliance-info",
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]
    ) -> None:
        if (
            nation := utils.regex_groups_to_model(
                interaction, groups, cache.get_nation, errors.NationNotFoundError
            )
        ) is None:
            return
        alliance = nation.alliance
        if alliance is None:
            raise errors.NationNotInAllianceError(nation)
        await interaction.respond_with_message(
            embed=alliance.build_embed(interaction),
            ephemeral=True,
        )
