from __future__ import annotations

from typing import Optional

from discord import ButtonStyle, Interaction, ui

__all__ = ("Confirm",)


class Confirm(ui.View):
    """
    self.interaction is available so the command can perform a result on it's own
    """

    value: Optional[bool]

    def __init__(self):
        super().__init__()
        self.value = None

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, button: ui.Button, interaction: Interaction) -> None:
        self.interaction = interaction
        self.value = True
        self.stop()

    @ui.button(label="No", style=ButtonStyle.red)
    async def no(self, button: ui.Button, interaction: Interaction) -> None:
        self.interaction = interaction
        self.value = False
