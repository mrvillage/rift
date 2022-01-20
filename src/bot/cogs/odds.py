from __future__ import annotations

import math
from typing import Dict

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...data.classes import Nation
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext


def get_casualties_air(attacker_aircraft: float, defender_aircraft: float):
    attacker_val = attacker_aircraft * 3
    defender_val = defender_aircraft * 3
    attacker_low = attacker_val * 0.4
    defender_low = defender_val * 0.4
    return {
        "attacker": {
            "low": min(defender_low * 0.01 * 3, attacker_aircraft),
            "high": min(defender_val * 0.01 * 3, attacker_aircraft),
        },
        "defender": {
            "low": min(attacker_low * 0.018337 * 3, defender_aircraft),
            "high": min(attacker_val * 0.018337 * 3, defender_aircraft),
        },
    }


def get_casualties_ground(
    attacker_soldiers: float,
    attacker_tanks: float,
    defender_soldiers: float,
    defender_tanks: float,
):
    # TODO SIMPLIFY
    attacker_val = (attacker_soldiers * 1.75) + (attacker_tanks * 40)
    defender_val = (defender_soldiers * 1.75) + (defender_tanks * 40)

    attacker_soldiers_val = attacker_soldiers * 1.75
    attacker_tanks_val = attacker_tanks * 40
    defender_soldiers_val = defender_soldiers * 1.75
    defender_tanks_val = defender_tanks * 40

    attacker_soldiers_low = attacker_soldiers * 1.75 * 0.4
    attacker_tanks_low = attacker_tanks * 40 * 0.4
    defender_soldiers_low = defender_soldiers * 1.75 * 0.4
    defender_tanks_low = defender_tanks * 40 * 0.4
    response: Dict[str, Dict[str, float]] = {
        "attacker": {
            "soldiers_low": 0,
            "soldiers_high": 0,
            "tanks_low": 0.0,
            "tanks_high": 0,
        },
        "defender": {
            "soldiers_low": 0,
            "soldiers_high": 0,
            "tanks_low": 0,
            "tanks_high": 0,
        },
    }
    response["attacker"]["soldiers_low"] = min(
        (defender_soldiers_low * 0.0084) + (defender_tanks_low * 0.0092) * 3,
        attacker_soldiers,
    )
    response["attacker"]["soldiers_high"] = min(
        (defender_soldiers_val * 0.0084) + (defender_tanks_val * 0.0092) * 3,
        attacker_soldiers,
    )
    response["defender"]["soldiers_low"] = min(
        (attacker_soldiers_low * 0.0084) + (attacker_tanks_low * 0.0092) * 3,
        defender_soldiers,
    )
    response["defender"]["soldiers_high"] = min(
        (attacker_soldiers_val * 0.0084) + (attacker_tanks_val * 0.0092) * 3,
        defender_soldiers,
    )
    if attacker_val > defender_val:

        response["attacker"]["tanks_low"] = min(
            (defender_soldiers_low * 0.0004060606)
            + ((defender_tanks_low * 0.00066666666)) * 3,
            attacker_tanks,
        )
        response["attacker"]["tanks_high"] = min(
            (defender_soldiers_val * 0.0004060606)
            + ((defender_tanks_val * 0.00066666666)) * 3,
            attacker_tanks,
        )
        response["defender"]["tanks_low"] = min(
            (attacker_soldiers_low * 0.00043225806)
            + ((attacker_tanks_low * 0.00070967741)) * 3,
            defender_tanks,
        )
        response["defender"]["tanks_high"] = min(
            (attacker_soldiers_val * 0.00043225806)
            + ((attacker_tanks_val * 0.00070967741)) * 3,
            defender_tanks,
        )
    else:
        response["defender"]["tanks_low"] = min(
            (defender_soldiers_low * 0.0004060606)
            + ((defender_tanks_low * 0.00066666666)) * 3,
            attacker_tanks,
        )
        response["defender"]["tanks_high"] = min(
            (defender_soldiers_val * 0.0004060606)
            + ((defender_tanks_val * 0.00066666666)) * 3,
            attacker_tanks,
        )
        response["attacker"]["tanks_low"] = min(
            (attacker_soldiers_low * 0.00043225806)
            + ((attacker_tanks_low * 0.00070967741)) * 3,
            defender_tanks,
        )
        response["attacker"]["tanks_high"] = min(
            (attacker_soldiers_val * 0.00043225806)
            + ((attacker_tanks_val * 0.00070967741)) * 3,
            defender_tanks,
        )
    return response


def get_casualties_naval(attacker_ships: float, defender_ships: float):
    attacker_val = attacker_ships * 4
    defender_val = defender_ships * 4
    attacker_low = attacker_val * 0.4
    defender_low = defender_val * 0.4
    chance_for_three = (
        0.01375 * 3
    )  # leaving this in here so we aren't confused looking back on the future

    # its attacker for defender because casualties are based on the opponents units

    # origanl vals are to make sure it doesnt go below zero, and its devided by 4 to get
    # the real number of casultys because this is only dealing with ships atm
    return {
        "attacker": {
            "low": min(defender_low * chance_for_three, attacker_ships),
            "high": min(defender_val * chance_for_three, attacker_ships),
        },
        "defender": {
            "low": min(attacker_low * chance_for_three, defender_ships),
            "high": min(attacker_val * chance_for_three, defender_ships),
        },
    }


def get_attack_chance(attacker_val: float, defender_val: float) -> Dict[str, float]:
    nwins: int = 0
    decplaces = 1000
    for i in range(decplaces):
        for n in range(decplaces):
            nwins += attacker_val - (
                (i * 0.6) / decplaces * attacker_val
            ) > defender_val - ((n * 0.6) / decplaces * defender_val)
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
        if attacker is MISSING and defender is MISSING:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one nation.",
            )
        attacker = attacker or await Nation.convert(ctx, attacker)
        defender = defender or await Nation.convert(ctx, defender)
        await ctx.response.defer()  # type: ignore
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

    @odds.command(  # type: ignore
        name="attacks",
        brief="Calculate the odds of two nations fighting",
        type=commands.CommandType.chat_input,
    )
    async def odds_attacks(
        self,
        ctx: RiftContext,
        attacker: Nation = MISSING,
        defender: Nation = MISSING,
    ):
        if attacker is MISSING and defender is MISSING:
            raise EmbedErrorMessage(
                ctx.author,
                "You must specify at least one nation.",
            )
        attacker = attacker or await Nation.convert(ctx, attacker)
        defender = defender or await Nation.convert(ctx, defender)
        await ctx.response.defer()  # type: ignore
        # FIXME doesnt include population reisistance
        ground_chance = get_attack_chance(
            (float(attacker.soldiers) * 1.75) + (attacker.tanks * 40),
            (float(defender.soldiers) * 1.75) + (defender.tanks * 40),
        )
        naval_chance = get_attack_chance(attacker.ships * 4, defender.ships * 4)
        air_chance = get_attack_chance(attacker.aircraft * 3, defender.aircraft * 3)

        naval_cas = get_casualties_naval(attacker.ships, defender.ships)
        ground_cas = get_casualties_ground(
            attacker.soldiers, attacker.tanks, defender.soldiers, defender.tanks
        )
        air_cas = get_casualties_air(attacker.aircraft, defender.aircraft)

        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{attacker} vs {defender}\n",
                fields=[
                    {
                        "name": "Ground Battle",
                        "value": f"Immense: {ground_chance['immense']:.2%}\nModerate:{ground_chance['moderate']:.2%}\nPyrrhic: {ground_chance['pyrrhic']:.2%}\nFailure:{ground_chance['failure']:.2%}\nAttacker Casualties: {math.floor(ground_cas['attacker']['soldiers_low']):,}-{math.ceil(ground_cas['attacker']['soldiers_high']):,} soldiers; {math.floor(ground_cas['attacker']['tanks_low']):,}-{math.ceil(ground_cas['attacker']['tanks_high']):,} tanks\nDefender Casualties: {math.floor(ground_cas['defender']['soldiers_low']):,}-{math.ceil(ground_cas['defender']['soldiers_high']):,} soldiers; {math.floor(ground_cas['defender']['tanks_low']):,}-{math.ceil(ground_cas['defender']['tanks_high']):,} tanks",
                    },
                    {
                        "name": "Air Battle",
                        "value": f"Immense: {air_chance['immense']:.2%}\nModerate: {air_chance['moderate']:.2%}\nPyrrhic: {air_chance['pyrrhic']:.2%}\nFailure: {air_chance['failure']:.2%}\nAttacker Casualties: {math.floor(air_cas['attacker']['low']):,}-{math.ceil(air_cas['attacker']['high']):,} aircraft\nDefender Casualties: {math.floor(air_cas['defender']['low']):,}-{math.ceil(air_cas['defender']['high']):,} aircraft",
                    },
                    {
                        "name": "Naval Battle",
                        "value": f"Immense: {naval_chance['immense']:.2%}\nModerate: {naval_chance['moderate']:.2%}\nPyrrhic: {naval_chance['pyrrhic']:.2%}\nFailure: {naval_chance['failure']:.2%}\nAttacker Casualties:{math.floor(naval_cas['attacker']['low']):,}-{math.ceil(naval_cas['attacker']['high']):,}\nDefender Casualties: {math.floor(naval_cas['defender']['low']):,}-{math.ceil(naval_cas['defender']['high']):,} ships",
                    },
                ],
                color=discord.Color.blue(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Odds(bot))
