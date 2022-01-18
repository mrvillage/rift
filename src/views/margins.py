from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ..cache import cache
from ..funcs import get_embed_author_member
from ..ref import ID

__all__ = ("Margins",)


class Margins(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(  # type: ignore
        label="Refresh", style=discord.ButtonStyle.gray, custom_id="MARGINS_REFRESH_1"
    )
    async def refresh(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        message = interaction.message
        if TYPE_CHECKING:
            assert isinstance(message, discord.Message)
        if message.embeds[0].title != "Trade Margins" or message.author.id != ID:  # type: ignore
            return
        prices = cache.prices
        if TYPE_CHECKING:
            assert isinstance(interaction.user, (discord.Member, discord.User))
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
