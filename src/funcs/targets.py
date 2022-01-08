from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, List, Tuple

import discord
from discord.utils import MISSING

from .. import funcs
from ..data.classes import AllianceSettings, Condition, Nation, Target
from ..errors import EmbedErrorMessage
from ..ref import RiftContext

__all__ = ("find_targets", "find_attackers")

if TYPE_CHECKING:
    from _typings import Field


async def find_targets(
    ctx: RiftContext,
    condition: Condition = MISSING,
    nation: Nation = MISSING,
    *,
    count_cities: bool = False,
    count_loot: bool = False,
    count_infrastructure: bool = False,
    count_military: bool = False,
    count_activity: bool = False,
    evaluate_alliance_raid_default: bool = False,
    evaluate_alliance_nuke_default: bool = False,
    evaluate_alliance_military_default: bool = False,
    offset: int = 0,
) -> Any:  # sourcery no-metrics
    await ctx.interaction.response.defer(ephemeral=True)
    nation = nation or await Nation.convert(ctx, nation)
    if nation.alliance is not None:
        settings = await AllianceSettings.fetch(nation.alliance.id)
        if (
            evaluate_alliance_raid_default
            and settings.default_raid_condition is not None
        ):
            default_condition = Condition.parse(settings.default_raid_condition)
            if condition is MISSING:
                condition = default_condition
            else:
                condition = Condition.union(condition, default_condition)
        if (
            evaluate_alliance_nuke_default
            and settings.default_nuke_condition is not None
        ):
            default_condition = Condition.parse(settings.default_nuke_condition)
            if condition is MISSING:
                condition = default_condition
            else:
                condition = Condition.union(condition, default_condition)
        if (
            evaluate_alliance_military_default
            and settings.default_military_condition is not None
        ):
            default_condition = Condition.parse(settings.default_military_condition)
            if condition is MISSING:
                condition = default_condition
            else:
                condition = Condition.union(condition, default_condition)
    targets = await nation.find_targets(condition, loot=count_loot)
    ratings: List[Tuple[float, Target]] = []
    for index, i in enumerate(targets):
        if i.nation is None:
            continue
        ratings.append(
            (
                i.rate(
                    nation,
                    count_cities=count_cities,
                    count_loot=count_loot,
                    count_infrastructure=count_infrastructure,
                    count_military=count_military,
                    count_activity=count_activity,
                ),
                i,
            )
        )
        if index % 100:
            await asyncio.sleep(0)
    ratings = sorted(ratings, key=lambda i: i[0], reverse=True)
    if not ratings[offset:]:
        raise EmbedErrorMessage(
            ctx.author,
            "No targets found.",
        )
    fields: List[Field] = []
    for target in ratings[offset:]:
        if len(fields) >= 12:
            break
        rating = target[0]
        target = target[1]
        nat = target.nation
        if nat is None:
            continue
        fields.append(
            target.field(target, nat, rating, count_loot, count_infrastructure)
        )
    counting: List[str] = []
    if count_loot:
        counting.append("loot")
    if count_infrastructure:
        counting.append("infrastructure")
    if count_military:
        counting.append("military")
    if count_activity:
        counting.append("activity")
    if len(counting) == 1:
        counting_str = f"{counting[0]}.\n"
    elif len(counting) == 2:
        counting_str = f"{counting[0]} and {counting[1]}.\n"
    elif len(counting) >= 3:
        counting_str = ", ".join(counting[:-1]) + f", and {counting[-1]}.\n"
    else:
        counting_str = ""
    defaults: List[str] = []
    if evaluate_alliance_raid_default:
        defaults.append("raid")
    if evaluate_alliance_nuke_default:
        defaults.append("nuke")
    if evaluate_alliance_military_default:
        defaults.append("military")
    if len(defaults) == 1:
        defaults_str = f"{defaults[0]}.\n"
    elif len(defaults) == 2:
        defaults_str = f"{defaults[0]} and {defaults[1]}.\n"
    elif len(defaults) >= 3:
        defaults_str = ", ".join(defaults[:-1]) + f", and {defaults[-1]}.\n"
    else:
        defaults_str = ""
    await ctx.reply(
        embed=funcs.get_embed_author_member(
            ctx.author,
            f"{len(ratings):,} targets found for [{nation}](https://politicsandwar.com/nation/id={nation.id}). Showing #{offset+1:,}-#{offset+12:,}\n{counting_str}{defaults_str}",
            fields=fields,
            color=discord.Color.green(),
        ),
        ephemeral=True,
    )


async def find_attackers(
    ctx: RiftContext,
    condition: Condition = MISSING,
    nation: Nation = MISSING,
    *,
    count_cities: bool = False,
    count_infrastructure: bool = False,
    count_military: bool = False,
    count_activity: bool = False,
    evaluate_alliance_raid_default: bool = False,
    evaluate_alliance_nuke_default: bool = False,
    evaluate_alliance_military_default: bool = False,
    offset: int = 0,
) -> Any:  # sourcery no-metrics
    await ctx.interaction.response.defer(ephemeral=True)
    nation = nation or await Nation.convert(ctx, nation)
    if nation.alliance is not None:
        settings = await AllianceSettings.fetch(nation.alliance.id)
        if (
            evaluate_alliance_raid_default
            and settings.default_attack_raid_condition is not None
        ):
            default_condition = Condition.parse(settings.default_attack_raid_condition)
            if condition is MISSING:
                condition = default_condition
            else:
                condition = Condition.union(condition, default_condition)
        if (
            evaluate_alliance_nuke_default
            and settings.default_attack_nuke_condition is not None
        ):
            default_condition = Condition.parse(settings.default_attack_nuke_condition)
            if condition is MISSING:
                condition = default_condition
            else:
                condition = Condition.union(condition, default_condition)
        if (
            evaluate_alliance_military_default
            and settings.default_attack_military_condition is not None
        ):
            default_condition = Condition.parse(
                settings.default_attack_military_condition
            )
            if condition is MISSING:
                condition = default_condition
            else:
                condition = Condition.union(condition, default_condition)
    targets = await nation.find_attackers(condition)
    ratings: List[Tuple[float, Target]] = []
    target = await Target.create(nation, None, None, None)
    for index, i in enumerate(targets):
        if i.nation is None:
            continue
        ratings.append(
            (
                target.rate(
                    i.nation,
                    count_cities=count_cities,
                    count_infrastructure=count_infrastructure,
                    count_military=count_military,
                    count_activity=count_activity,
                ),
                i,
            )
        )
        if index % 100:
            await asyncio.sleep(0)
    ratings = sorted(ratings, key=lambda i: i[0], reverse=True)
    if not ratings[offset:]:
        raise EmbedErrorMessage(
            ctx.author,
            "No attackers found.",
        )
    fields: List[Field] = []
    for target in ratings[offset:]:
        if len(fields) >= 12:
            break
        rating = target[0]
        target = target[1]
        nat = target.nation
        if nat is None:
            continue
        fields.append(target.field(target, nat, rating, count_infrastructure))
    counting: List[str] = []
    if count_infrastructure:
        counting.append("infrastructure")
    if count_military:
        counting.append("military")
    if count_activity:
        counting.append("activity")
    if len(counting) == 1:
        counting_str = f"{counting[0]}.\n"
    elif len(counting) == 2:
        counting_str = f"{counting[0]} and {counting[1]}.\n"
    elif len(counting) >= 3:
        counting_str = ", ".join(counting[:-1]) + f", and {counting[-1]}.\n"
    else:
        counting_str = ""
    defaults: List[str] = []
    if evaluate_alliance_raid_default:
        defaults.append("raid")
    if evaluate_alliance_nuke_default:
        defaults.append("nuke")
    if evaluate_alliance_military_default:
        defaults.append("military")
    if len(defaults) == 1:
        defaults_str = f"{defaults[0]}.\n"
    elif len(defaults) == 2:
        defaults_str = f"{defaults[0]} and {defaults[1]}.\n"
    elif len(defaults) >= 3:
        defaults_str = ", ".join(defaults[:-1]) + f", and {defaults[-1]}.\n"
    else:
        defaults_str = ""
    await ctx.reply(
        embed=funcs.get_embed_author_member(
            ctx.author,
            f"{len(ratings):,} attackers found for [{nation}](https://politicsandwar.com/nation/id={nation.id}). Showing #{offset+1:,}-#{offset+12:,}\n{counting_str}{defaults_str}",
            fields=fields,
            color=discord.Color.green(),
        ),
        ephemeral=True,
    )
