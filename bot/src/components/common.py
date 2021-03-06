from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import utils

__all__ = ("CommonButton", "CommonSelectMenu", "CommonGrid")

if TYPE_CHECKING:
    ...


class CommonButton(quarrel.Button):
    __slots__ = ()

    async def on_error(
        self, interaction: quarrel.Interaction, error: Exception
    ) -> None:
        if await utils.handle_interaction_error(interaction, error):
            await quarrel.Button.on_error(self, interaction, error)


class CommonSelectMenu(quarrel.SelectMenu):
    __slots__ = ()

    async def on_error(
        self, interaction: quarrel.Interaction, values: tuple[str], error: Exception
    ) -> None:

        # original = error
        if await utils.handle_interaction_error(interaction, error):
            await quarrel.SelectMenu.on_error(self, interaction, values, error)


class CommonGrid(quarrel.Grid):
    __slots__ = ()
