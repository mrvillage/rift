from __future__ import annotations

from typing import TYPE_CHECKING, List

import discord

from ..data.get import get_colors, get_nation_color_counts
from ..funcs import get_embed_author_member
from ..ref import ID

__all__ = ("Colors",)

if TYPE_CHECKING:
    from _typings import Field


class Colors(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Refresh", style=discord.ButtonStyle.gray, custom_id="COLORS_REFRESH_1"
    )
    async def refresh(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        message = interaction.message
        if TYPE_CHECKING:
            assert isinstance(message, discord.Message)
            assert isinstance(interaction.user, (discord.Member, discord.User))
        if (
            not message.embeds[0].description.startswith("Average Bonus:")  # type: ignore
            or message.author.id != ID
        ):
            return
        colors = await get_colors()
        nations = await get_nation_color_counts()
        average_bonus = (
            sum(i.bonus for i in colors.values() if i.color not in {"beige", "gray"})
            / len(colors)
        ) - 2
        fields: List[Field] = [
            {
                "name": i.color.capitalize(),
                "value": f"Name: {i.name}\nTurn Bonus: ${i.bonus:,.0f}\nNations on Color: {nations[i.color.capitalize()]:,}",
            }
            for i in colors.values()
        ]
        await interaction.response.edit_message(
            view=self,
            embed=get_embed_author_member(
                interaction.user,
                f"Average Bonus: ${average_bonus:,.2f}",
                fields=fields,
                color=discord.Color.blue(),
            ),
        )
