from __future__ import annotations

from typing import Dict

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...data.classes import Nation
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext


def get_attack_chance(attackerval: float, defenderval: float) -> Dict[str, float]:
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

    @odds.command(  # type: ignore
        name="attacks",
        brief="Calculate the odds of 2 nations fighting",
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

        groundChance = get_attack_chance(
            (float(attacker.soldiers) * 1.75) + (attacker.tanks * 40),
            (float(defender.soldiers) * 1.75) + (attacker.tanks * 40),
        )
        navalChance = get_attack_chance(attacker.ships * 4, defender.ships * 4)
        airChance = get_attack_chance(attacker.aircraft * 3, defender.aircraft * 3)

        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{attacker} vs {defender}\n",
                fields=[
                    {
                        "name": "Ground Battle",
                        "value": f"Immense:{groundChance['immense']*100}%, Moderate:{groundChance['moderate']*100}%, Pyrrhic:{groundChance['pyrrhic']*100}%, Failure:{groundChance['failure']*100}%,",
                    },
                    {
                        "name": "Air Battle",
                        "value": f"Immense:{airChance['immense']*100}%, Moderate:{airChance['moderate']*100}%, Pyrrhic:{airChance['pyrrhic ']*100}%, Failure:{airChance['failure']*100}%,",
                    },
                    {
                        "name": "Naval Battle",
                        "value": f"Immense:{navalChance['immense']*100}%, Moderate:{navalChance['moderate']*100}%, Pyrrhic:{navalChance['pyrrhic']*100}%, Failure:{navalChance['failure']*100}%,",
                    },
                ],
                color=discord.Color.blue(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Odds(bot))
