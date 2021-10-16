from __future__ import annotations

from typing import Optional

import discord
from discord.ext import commands

from ... import funcs
from ...data.classes import Nation
from ...ref import Rift, RiftContext


class Odds(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="odds",
        brief="Calculate the odds of success against a nation.",
        type=commands.CommandType.chat_input,
    )
    async def odds(self, ctx: RiftContext):
        ...

    @odds.command(  # type: ignore
        name="spies",
        brief="Calculate spy odds between two nations.",
        type=commands.CommandType.chat_input,
    )
    async def odds_spies(
        self,
        ctx: RiftContext,
        attacker: Optional[Nation] = None,
        defender: Optional[Nation] = None,
    ):
        await ctx.response.defer()  # type: ignore
        if attacker is None and defender is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You must specify at least one nation.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        attacker = attacker or await Nation.convert(ctx, attacker)
        defender = defender or await Nation.convert(ctx, defender)
        attacker_spies = await attacker.calculate_spies()
        defender_spies = await defender.calculate_spies()
        odds_1 = 1 * 25 + (attacker_spies * 100 / ((defender_spies * 3) + 1))
        odds_2 = 2 * 25 + (attacker_spies * 100 / ((defender_spies * 3) + 1))
        odds_3 = 3 * 25 + (attacker_spies * 100 / ((defender_spies * 3) + 1))
        modifier = (
            1.15
            if defender.war_policy == "Tactician"
            else 0.85
            if defender.war_policy == "Arcane"
            else 1
        )
        modifier = modifier * 1.15 if attacker.war_policy == "Covert" else modifier
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{attacker} vs {defender}\n{attacker_spies} Spies vs {defender_spies} Spies\nOdds are ordered for safety level 1, 2, 3 (Quick and Dirty, Normal Precautions, Extremely Covert).",
                fields=[
                    {
                        "name": "Gather Intelligence",
                        "value": f"{odds_1*modifier:,.2f}, {odds_2*modifier:,.2f}, {odds_3*modifier:,.2f}",
                    }
                ],
                color=discord.Color.blue(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Odds(bot))
