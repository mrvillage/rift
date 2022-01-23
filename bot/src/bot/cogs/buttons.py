from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ...cache import cache
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext

if TYPE_CHECKING:
    from typing import Optional, Union


class ButtonContext:
    def __init__(
        self,
        author: Union[discord.User, discord.Member],
        guild: Optional[discord.Guild],
    ):
        self.author: Union[discord.User, discord.Member] = author
        self.guild: Optional[discord.Guild] = guild


class Buttons(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.user is None:
            return
        custom_id = (
            interaction.data.get("custom_id") if interaction.data is not None else None
        )
        if custom_id is None:
            return
        parts = custom_id.split("-")
        if parts[0] != "info" or len(parts) != 3:
            return
        model = parts[1]
        try:
            model_id = int(parts[2])
        except ValueError:
            return
        ctx: RiftContext = ButtonContext(interaction.user, interaction.guild)  # type: ignore
        try:
            if model == "nation":
                nation = cache.get_nation(model_id)
                if nation is None:
                    raise EmbedErrorMessage(interaction.user, "No nation found.")
                await interaction.response.send_message(
                    embed=nation.get_info_embed(ctx),
                    view=nation.get_info_view(),
                    ephemeral=True,
                )
            elif model == "alliance":
                alliance = cache.get_alliance(model_id)
                if alliance is None:
                    raise EmbedErrorMessage(interaction.user, "No alliance found.")
                await interaction.response.send_message(
                    embed=alliance.get_info_embed(ctx),
                    ephemeral=True,
                )
        except EmbedErrorMessage as e:
            await interaction.response.send_message(
                embed=e.embed,
                ephemeral=e.ephemeral,
            )


def setup(bot: Rift):
    bot.add_cog(Buttons(bot))
