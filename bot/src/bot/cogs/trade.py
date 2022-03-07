from __future__ import annotations

import inspect

import discord
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...ref import Rift, RiftContext
from ...views import Margins, Prices


class Trade(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.command(
        name="prices",
        aliases=["p", "resource", "price"],
        brief="Get the current prices of all resources.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def prices(self, ctx: RiftContext):
        prices = cache.prices
        await ctx.reply(
            view=Prices(),
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Market Index: ${prices.market_index:,}",
                fields=[
                    {
                        "name": "Credits",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.credit.avg_price:,}
                Highest Buy: ${prices.credit.highest_buy.price:,} ({prices.credit.highest_buy.amount:,} Credits)
                Lowest Sell: ${prices.credit.lowest_sell.price:,} ({prices.credit.lowest_sell.amount:,} Credits)
                Trade Margin: ${prices.credit.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Food",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.food.avg_price:,}
                Highest Buy: ${prices.food.highest_buy.price:,} ({prices.food.highest_buy.amount:,} Food)
                Lowest Sell: ${prices.food.lowest_sell.price:,} ({prices.food.lowest_sell.amount:,} Food)
                Trade Margin: ${prices.food.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Coal",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.coal.avg_price:,}
                Highest Buy: ${prices.coal.highest_buy.price:,} ({prices.coal.highest_buy.amount:,} Coal)
                Lowest Sell: ${prices.coal.lowest_sell.price:,} ({prices.coal.lowest_sell.amount:,} Coal)
                Trade Margin: ${prices.coal.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Oil",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.oil.avg_price:,}
                Highest Buy: ${prices.oil.highest_buy.price:,} ({prices.oil.highest_buy.amount:,} Oil)
                Lowest Sell: ${prices.oil.lowest_sell.price:,} ({prices.oil.lowest_sell.amount:,} Oil)
                Trade Margin: ${prices.oil.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Uranium",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.uranium.avg_price:,}
                Highest Buy: ${prices.uranium.highest_buy.price:,} ({prices.uranium.highest_buy.amount:,} Uranium)
                Lowest Sell: ${prices.uranium.lowest_sell.price:,} ({prices.uranium.lowest_sell.amount:,} Uranium)
                Trade Margin: ${prices.uranium.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Lead",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.lead.avg_price:,}
                Highest Buy: ${prices.lead.highest_buy.price:,} ({prices.lead.highest_buy.amount:,} Lead)
                Lowest Sell: ${prices.lead.lowest_sell.price:,} ({prices.lead.lowest_sell.amount:,} Lead)
                Trade Margin: ${prices.lead.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Iron",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.iron.avg_price:,}
                Highest Buy: ${prices.iron.highest_buy.price:,} ({prices.iron.highest_buy.amount:,} Iron)
                Lowest Sell: ${prices.iron.lowest_sell.price:,} ({prices.iron.lowest_sell.amount:,} Iron)
                Trade Margin: ${prices.iron.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Bauxite",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.bauxite.avg_price:,}
                Highest Buy: ${prices.bauxite.highest_buy.price:,} ({prices.bauxite.highest_buy.amount:,} Bauxite)
                Lowest Sell: ${prices.bauxite.lowest_sell.price:,} ({prices.bauxite.lowest_sell.amount:,} Bauxite)
                Trade Margin: ${prices.bauxite.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Gasoline",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.gasoline.avg_price:,}
                Highest Buy: ${prices.gasoline.highest_buy.price:,} ({prices.gasoline.highest_buy.amount:,} Gasoline)
                Lowest Sell: ${prices.gasoline.lowest_sell.price:,} ({prices.gasoline.lowest_sell.amount:,} Gasoline)
                Trade Margin: ${prices.gasoline.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Munitions",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.munitions.avg_price:,}
                Highest Buy: ${prices.munitions.highest_buy.price:,} ({prices.munitions.highest_buy.amount:,} Munitions)
                Lowest Sell: ${prices.munitions.lowest_sell.price:,} ({prices.munitions.lowest_sell.amount:,} Munitions)
                Trade Margin: ${prices.munitions.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Steel",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.steel.avg_price:,}
                Highest Buy: ${prices.steel.highest_buy.price:,} ({prices.steel.highest_buy.amount:,} Steel)
                Lowest Sell: ${prices.steel.lowest_sell.price:,} ({prices.steel.lowest_sell.amount:,} Steel)
                Trade Margin: ${prices.steel.trade_margin:,}
                """
                        ),
                    },
                    {
                        "name": "Aluminum",
                        "value": inspect.cleandoc(
                            f"""
                Market Price: ${prices.aluminum.avg_price:,}
                Highest Buy: ${prices.aluminum.highest_buy.price:,} ({prices.aluminum.highest_buy.amount:,} Aluminum)
                Lowest Sell: ${prices.aluminum.lowest_sell.price:,} ({prices.aluminum.lowest_sell.amount:,} Aluminum)
                Trade Margin: ${prices.aluminum.trade_margin:,}
                """
                        ),
                    },
                ],
                color=discord.Color.blue(),
            ),
        )

    @commands.command(
        name="margins",
        aliases=["trade-margin", "trademargin", "margin", "tm"],
        brief="Get the current trade margins.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
    )
    async def margins(self, ctx: RiftContext):
        prices = cache.prices
        await ctx.reply(
            view=Margins(),
            embed=funcs.get_embed_author_member(
                ctx.author,
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


def setup(bot: Rift):
    bot.add_cog(Trade(bot))