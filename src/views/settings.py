from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from .. import funcs
from .confirm import Confirm

__all__ = ("AlliancePurposeConfirm",)

if TYPE_CHECKING:
    from ..data.classes import Alliance, GuildSettings


class AlliancePurposeConfirm(Confirm):
    purpose: str
    alliance: Alliance
    user: discord.User
    settings: GuildSettings
    message: discord.Message

    def __init__(
        self,
        purpose: str,
        alliance: Alliance,
        user: discord.User,
        settings: GuildSettings,
    ):
        self.purpose = purpose
        self.alliance = alliance
        self.user = user
        self.settings = settings
        super().__init__(timeout=900)

    async def start(self) -> None:
        self.message = await self.user.send(
            embed=funcs.get_embed_author_member(
                self.user,
                description=f"**NOTE: IF YOU DO NOT RECOGNIZE THIS MESSAGE, UNDER NO CIRCUMSTANCES HIT YES**\n\nAre you sure you want to set the server purpose to `{self.purpose}` and link it to {repr(self.alliance)}?",
                color=discord.Color.gold(),
            ),
            view=self,
        )

    async def hook(self, interaction: discord.Interaction) -> None:
        if self.value:
            await self.settings.set_(
                purpose=self.purpose, purpose_argument=str(self.alliance.id)
            )
            await self.message.edit(
                embed=funcs.get_embed_author_member(
                    self.user,
                    description=f"The server purpose has been set to `{self.purpose}` and has been linked to {repr(self.alliance)}.",
                    color=discord.Color.green(),
                ),
                view=None,
            )
        else:
            await self.message.edit(
                embed=funcs.get_embed_author_member(
                    self.user,
                    description=f"The request to set the server purpose has been denied.",
                    color=discord.Color.red(),
                ),
                view=None,
            )

    async def on_timeout(self) -> None:
        await self.message.edit(
            embed=funcs.get_embed_author_member(
                self.user,
                "Purpose change timed out. Please try again.",
                color=discord.Color.red(),
            ),
            view=None,
        )
