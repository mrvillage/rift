from __future__ import annotations

import quarrel

from .. import cache, errors, models, utils
from .common import CommonButton, CommonGrid

__all__ = ("NationGrid",)


class NationGrid(CommonGrid):
    def __init__(self, nation: models.Nation) -> None:
        super().__init__(timeout=None)
        self.nation: models.Nation = nation


class NationAllianceInformationButton(CommonButton):
    def __init__(self) -> None:
        super().__init__(
            label="Alliance Information",
            style=quarrel.ButtonStyle.GRAY,
            pattern="info-nation-([0-9]+?P<nation_id>)-alliance",
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
