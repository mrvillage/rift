from __future__ import annotations

import discord

__all__ = ("Info",)


class Info(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)
        self.stop()

    def add_button(self, name: str, value: str) -> Info:
        self.add_item(  # type: ignore
            discord.ui.Button(
                label=name, style=discord.ButtonStyle.gray, custom_id=value
            )
        )
        return self

    def add_url(self, name: str, url: str) -> Info:
        self.add_item(discord.ui.Button(label=name, url=url))  # type: ignore
        return self
