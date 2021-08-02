from __future__ import annotations
from typing import TYPE_CHECKING
from ... import funcs

import discord
from discord.ext import commands
import pnwkit

from ...data.classes import Nation, TradePrices
from ...ref import Rift


class HouseStark(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.command(name="mmr")
    async def mmr(self, ctx: commands.Context, *, nation: Nation = None):
        nation = nation or await Nation.convert(ctx, nation)
        author_nation = await Nation.convert(ctx, None)
        if nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Stockpiles doesn't apply to that nation!",
                    color=discord.Color.red(),
                )
            )
            return
        if author_nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
            return
        mmr = {
            "soldiers": 0 * 3000 * nation.cities,
            "tanks": 2 * 250 * nation.cities,
            "aircraft": 5 * 15 * nation.cities,
            "ships": 0 * 5 * nation.cities,
        }
        if all(getattr(nation, key) >= mmr[key] for key in mmr):
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, f"{nation} meets MMR!", color=discord.Color.green()
                )
            )
            return
        amounts = "\n".join(
            f"**{key.capitalize()}** - {getattr(nation, key)}/{mmr[key]} ({getattr(nation, key)/mmr[key]:.2%})"
            for key in mmr
            if getattr(nation, key) < mmr[key]
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{nation} doesn't meet MMR!\n\n{amounts}",
                color=discord.Color.orange(),
            )
        )

    @commands.command(name="stockpile", aliases=["stockpiles"])
    async def stockpile(self, ctx: commands.Context, *, nation: Nation = None):
        nation = nation or await Nation.convert(ctx, nation)
        nat = await pnwkit.async_nation_query(
            {"id": nation.id},
            "money",
            "food",
            "uranium",
            "steel",
            "aluminum",
            "gasoline",
            "munitions",
        )
        if TYPE_CHECKING:
            assert isinstance(nat, tuple)
        nat = nat[0]
        author_nation = await Nation.convert(ctx, None)
        if nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Stockpiles doesn't apply to that nation!",
                    color=discord.Color.red(),
                )
            )
            return
        if author_nation.alliance_id not in {3683, 8139}:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You don't have permission to use that command!!",
                    color=discord.Color.red(),
                )
            )
            return
        stockpile = {
            "money": 1000000 * nation.cities,
            "food": 10000 + (2000 * nation.cities),
            "uranium": 100 * nation.cities,
            "steel": 3000 * nation.cities,
            "aluminum": 1000 * nation.cities,
            "gasoline": 3600 * nation.cities,
            "munitions": 5400 * nation.cities,
        }
        if all(getattr(nat, key) >= stockpile[key] for key in stockpile):
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"{nation} meets stockpiles!",
                    color=discord.Color.green(),
                )
            )
            return
        prices: TradePrices = await funcs.get_trade_prices()
        amounts = []
        cost = 0
        for key, needs in stockpile.items():
            has = getattr(nat, key)
            if has < needs:
                price = getattr(prices, key)
                amount = (needs - has) * price.lowest_sell.price
                cost += amount
                amounts.append(
                    f"**{key.capitalize()}** - {has}/{needs} ({has/needs:.2%})\n${amount:,.2f} for {needs-has:,.2f}"
                )
        amounts = "\n".join(amounts)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{nation} doesn't meet stockpiles!\n\n{amounts}\n\n**Total:** ${cost:,.2f}",
                color=discord.Color.orange(),
            )
        )


def setup(bot: Rift) -> None:
    bot.add_cog(HouseStark(bot))
