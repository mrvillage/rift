from __future__ import annotations

from discord.ui import ButtonStyle


class ButtonStyle(ButtonStyle):
    def __get_item__(self: ButtonStyle, name: str):
        self.__getattr__(name)
