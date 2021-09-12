from __future__ import annotations

from typing import Optional

from discord import ButtonStyle, Interaction, ui

__all__ = ("Confirm",)


class Confirm(ui.View):
    """
    self.interaction is available so the command can perform a result
    on it's own or can define self.hook in a subclass
    """

    value: Optional[bool]

    def __init__(self):
        super().__init__()
        self.value = None

    async def hook(self, interaction: Interaction):
        pass

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, button: ui.Button, interaction: Interaction):
        self.interaction = interaction
        self.value = True
        self.stop()
        await self.hook(interaction)

    @ui.button(label="No", style=ButtonStyle.red)
    async def no(self, button: ui.Button, interaction: Interaction):
        self.interaction = interaction
        self.value = False
        self.stop()
        await self.hook(interaction)
