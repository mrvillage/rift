from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import ButtonStyle, Interaction, Member, Message, User, ui

from ..data.get import get_colors, get_nation_color_counts
from ..env import APPLICATION_ID
from ..funcs import get_embed_author_member

__all__ = ("Colors",)


class Colors(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Refresh", style=ButtonStyle.gray, custom_id="COLORS_REFRESH_1")
    async def refresh(self, button: ui.Button, interaction: Interaction):
        message = interaction.message
        if TYPE_CHECKING:
            assert isinstance(message, Message)
        if (
            message.embeds[0].description.startswith("Average Bonus:")
            and message.author.id != APPLICATION_ID
        ):
            return
        if TYPE_CHECKING:
            assert isinstance(interaction.user, (Member, User))
        colors = await get_colors()
        nations = await get_nation_color_counts()
        average_bonus = (
            sum(i.bonus for i in colors.values() if i.color not in {"beige", "gray"})
            / len(colors)
        ) - 2
        fields = [
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
