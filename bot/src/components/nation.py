from __future__ import annotations

import quarrel

from .common import CommonButton, CommonGrid

__all__ = ("NationGrid",)


class NationGrid(CommonGrid):
    ...


class AllianceInformationButton(CommonButton):
    def __init__(self) -> None:
        super().__init__(label="Alliance Information", style=quarrel.ButtonStyle.GRAY)

    async def callback(self, interaction: quarrel.Interaction, groups: quarrel.Missing[dict[str, str]]) -> None:
        ...
