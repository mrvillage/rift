from __future__ import annotations

from typing import Optional

import discord

__all__ = ("Confirm",)


class Confirm(discord.ui.View):
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

    async def hook(self, interaction: discord.Interaction):
        if self.defer:
            await interaction.response.defer()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green) # type: ignore
    async def yes(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        self.interaction = interaction
        self.value = True
        await self.hook(interaction)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red) # type: ignore
    async def no(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        self.interaction = interaction
        self.value = False
        await self.hook(interaction)
        self.stop()
