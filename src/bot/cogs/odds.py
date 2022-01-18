from __future__ import annotations

from typing import Dict

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...data.classes import Nation
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext


def get_attack_chance(attackerval: int, defenderval: int) -> Dict[str, float]:
    nwins: int = 0
    decplaces = 1000
    for i in range(decplaces):
        for n in range(decplaces):
            nwins += attackerval - (
                (i * 0.6) / decplaces * attackerval
            ) > defenderval - ((n * 0.6) / decplaces * defenderval)
    chance = nwins / (decplaces ** 2)
    unchance = 1 - chance
    immense = chance ** 3
    moderate = chance * chance * unchance * 3
    pyrrhic = chance * unchance * unchance * 3
    failure = unchance ** 3
    return {
        "failure": failure,
        "pyrrhic": pyrrhic,
        "moderate": moderate,
        "immense": immense,
    }


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
        attacker: Nation = MISSING,
        defender: Nation = MISSING,
    ):
        await ctx.response.defer()  # type: ignore
        if attacker is MISSING and defender is MISSING:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one nation.",
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

    @odds.group(
        name="battles",
        brief="calculate the odds of a battle winning or losing",
        type=commands.CommandType.chat_input,
    )
    async def odds_battles(self, ctx: RiftContext):
        ...

    @odds_battles.command(  # type: ignore
        name="naval",
        brief="Calculate naval battle odds between two nations",
        type=commands.CommandType.chat_input,
    )
    async def odds_battles_naval(
        self,
        ctx: RiftContext,
        attacker: Nation = MISSING,
        defender: Nation = MISSING,
    ):
        await ctx.response.defer()  # type: ignore
        if attacker is MISSING and defender is MISSING:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one nation.",
            )
        attacker = attacker or await Nation.convert(ctx, attacker)
        defender = defender or await Nation.convert(ctx, defender)

        response = get_attack_chance(attacker.ships, defender.ships)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{attacker} vs {defender}\n{attacker.ships} Spies vs {defender.ships} Spies\nOdds are ordered for safety level 1, 2, 3 (Quick and Dirty, Normal Precautions, Extremely Covert).",
                fields=[
                    {
                        "name": "Immense Triumph",
                        "value": f"{response['immense']}",
                    },
                    {
                        "name": "Moderate Success",
                        "value": f"{response['moderate']}",
                    },
                    {
                        "name": "Pyrrhic Victory",
                        "value": f"{response['pyrrhic']}",
                    },
                    {
                        "name": "Utter Failure",
                        "value": f"{response['failure']}",
                    },
                ],
                color=discord.Color.blue(),
            )
        )

    @odds_battles.command(  # type: ignore
        name="ground",
        brief="Calculate ground battle odds between two nations",
        type=commands.CommandType.chat_input,
    )
    async def odds_battles_ground(
        self,
        ctx: RiftContext,
        attacker: Nation = MISSING,
        defender: Nation = MISSING,
    ):
        await ctx.response.defer()  # type: ignore
        if attacker is MISSING and defender is MISSING:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one nation.",
            )
        attacker = attacker or await Nation.convert(ctx, attacker)
        defender = defender or await Nation.convert(ctx, defender)

    @odds_battles.command(  # type: ignore
        name="air",
        brief="Calculate air battle odds between two nations",
        type=commands.CommandType.chat_input,
    )
    async def odds_battles_air(
        self,
        ctx: RiftContext,
        attacker: Nation = MISSING,
        defender: Nation = MISSING,
    ):
        await ctx.response.defer()  # type: ignore
        if attacker is MISSING and defender is MISSING:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one nation.",
            )
        attacker = attacker or await Nation.convert(ctx, attacker)
        defender = defender or await Nation.convert(ctx, defender)


def setup(bot: Rift):
    bot.add_cog(Odds(bot))
