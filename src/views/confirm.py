from typing import Optional

from discord import Interaction
from .. import ui


class Confirm(ui.View):
    """
    self.interaction is available so the command can perform a result on it's own
    """

    value: Optional[bool]

    def __init__(self):
        super().__init__()
        self.value = None

    @ui.button(label="Yes", style=ui.ButtonStyle.green)
    async def yes(self, button: ui.Button, interaction: Interaction) -> None:
        self.interaction = interaction
        self.value = True
        self.stop()

    @ui.button(label="No", style=ui.ButtonStyle.red)
    async def no(self, button: ui.Button, interaction: Interaction) -> None:
        self.interaction = interaction
        self.value = False
