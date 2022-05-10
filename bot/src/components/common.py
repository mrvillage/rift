from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import utils

__all__ = ("CommonButton", "CommonSelectMenu", "CommonGrid")

if TYPE_CHECKING:
    ...


class CommonButton(quarrel.Button):
    async def on_error(
        self, interaction: quarrel.Interaction, error: Exception
    ) -> None:
        if utils.handle_interaction_error(interaction, error):
            await quarrel.Button.on_error(self, error)  # type: ignore


class CommonSelectMenu(quarrel.SelectMenu):
    async def on_error(
        self, interaction: quarrel.Interaction, values: tuple[str], error: Exception
    ) -> None:

        # original = error
        if utils.handle_interaction_error(interaction, error):
            await quarrel.Button.on_error(self, error)  # type: ignore


class CommonGrid(quarrel.Grid):
    ...
