from __future__ import annotations

from discord.enums import ButtonStyle


class ButtonStyle(ButtonStyle):
    def __get_item__(self, name: str):
        self.__getattr__(name)
