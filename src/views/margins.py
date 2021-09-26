from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import ButtonStyle, Interaction, Member, Message, User, ui

from ..env import APPLICATION_ID
from ..funcs import get_embed_author_member, get_trade_prices

__all__ = ("Margins",)


class Margins(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Refresh", style=ButtonStyle.gray, custom_id="MARGINS_REFRESH_1")
    async def refresh(self, button: ui.Button, interaction: Interaction):
        message = interaction.message
        if TYPE_CHECKING:
            assert isinstance(message, Message)
        if (
            message.embeds[0].title != "Trade Margins"
            and message.author.id != APPLICATION_ID
        ):
            return
        prices = await get_trade_prices()
        if TYPE_CHECKING:
            assert isinstance(interaction.user, (Member, User))
        await interaction.response.edit_message(
            view=self,
            embed=get_embed_author_member(
                interaction.user,
                f"Market Index: ${prices.market_index:,}",
                title="Trade Margins",
                fields=[
                    {
                        "name": "Credits",
                        "value": f"""
            ${prices.credit.trade_margin:,}
            """,
                    },
                    {
                        "name": "Food",
                        "value": f"""
            ${prices.food.trade_margin:,}
            """,
                    },
                    {
                        "name": "Coal",
                        "value": f"""
            ${prices.coal.trade_margin:,}
            """,
                    },
                    {
                        "name": "Oil",
                        "value": f"""
            ${prices.oil.trade_margin:,}
            """,
                    },
                    {
                        "name": "Uranium",
                        "value": f"""
            ${prices.uranium.trade_margin:,}
            """,
                    },
                    {
                        "name": "Lead",
                        "value": f"""
            ${prices.lead.trade_margin:,}
            """,
                    },
                    {
                        "name": "Iron",
                        "value": f"""
            ${prices.iron.trade_margin:,}
            """,
                    },
                    {
                        "name": "Bauxite",
                        "value": f"""
            ${prices.bauxite.trade_margin:,}
            """,
                    },
                    {
                        "name": "Gasoline",
                        "value": f"""
            ${prices.gasoline.trade_margin:,}
            """,
                    },
                    {
                        "name": "Munitions",
                        "value": f"""
            ${prices.munitions.trade_margin:,}
            """,
                    },
                    {
                        "name": "Steel",
                        "value": f"""
            ${prices.steel.trade_margin:,}
            """,
                    },
                    {
                        "name": "Aluminum",
                        "value": f"""
            ${prices.aluminum.trade_margin:,}
            """,
                    },
                ],
            color=discord.Color.blue(),
            ),
        )
