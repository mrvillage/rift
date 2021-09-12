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
    defer: bool

    def __init__(self, timeout: Optional[float] = 180, defer: bool = False):
        super().__init__(timeout=timeout)
        self.value = None
        self.defer = defer

    async def hook(self, interaction: Interaction):
        if self.defer:
            await interaction.response.defer()

    @ui.button(label="Yes", style=ButtonStyle.green)
    async def yes(self, button: ui.Button, interaction: Interaction):
        self.interaction = interaction
        self.value = True
        await self.hook(interaction)
        self.stop()

    @ui.button(label="No", style=ButtonStyle.red)
    async def no(self, button: ui.Button, interaction: Interaction):
        self.interaction = interaction
        self.value = False
        await self.hook(interaction)
        self.stop()
