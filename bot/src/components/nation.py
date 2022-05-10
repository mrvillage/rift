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
        self.add_component(NationAllianceInformationButton(nation))


@bot.component
class NationAllianceInformationButton(CommonButton):
    def __init__(self, nation: Missing[models.Nation] = quarrel.MISSING) -> None:
        super().__init__(
            custom_id=f"info-nation-{nation.id}-alliance"
            if nation
            else quarrel.MISSING,
            label="Alliance Information",
            style=quarrel.ButtonStyle.GRAY,
            pattern="info-nation-(?P<nation_id>[0-9]+)-alliance",
        )

    async def callback(
        self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]
    ) -> None:
        if groups is quarrel.MISSING:
            return
        try:
            nation_id = utils.convert_int(groups["nation_id"])
        except ValueError:
            return
        nation = cache.get_nation(nation_id)
        if nation is None:
            raise errors.NationNotFoundError(interaction, nation_id)
        alliance = nation.alliance
        if alliance is None:
            raise errors.NationNotInAllianceError(nation)
        await interaction.respond_with_message(
            embed=alliance.build_embed(interaction.user),
            ephemeral=True,
        )
