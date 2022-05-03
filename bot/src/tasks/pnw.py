from __future__ import annotations

import asyncio
import datetime
from typing import TYPE_CHECKING

import attrs
import pnwkit

from .. import cache, models, utils
from ..bot import bot
from ..env import kit
from .common import CommonTask

__all__ = ("PnWDataTask",)

if TYPE_CHECKING:
    from typing import Any, Callable, Optional


async def handle_model_update(
    name: str,
    model: Any,
    paginator: pnwkit.Paginator[Any],
    current: set[Any],
    adder: Callable[[Any], Any],
    getter: Callable[[int], Any],
    remover: Callable[[Any], Any],
    no_compare: Optional[list[str]] = None,
    *,
    delete: bool = True,
    batch_size: int = 10,
) -> None:
    # data_dict: dict[int, Any] = {}
    # try:
    #     async for i in paginator.batch(5):
    #         data_dict[int(i.id)] = model.from_data(i)
    # except Exception as error:
    #     pass
    data_dict = {
        int(i.id): model.from_data(i) async for i in paginator.batch(batch_size)
    }
    ids = set(data_dict.keys())
    current_ids = {i.id for i in current}
    deleted_ids = current_ids - ids
    created_ids = ids - current_ids
    updated_ids = ids & current_ids
    if delete:
        for i in deleted_ids:
            old = cache.get_alliance(i)
            if old is not None:
                remover(old)
                await old.delete()
                bot.dispatch(f"{name}_delete", old)
    for i in created_ids:
        new = data_dict[i]
        adder(new)
        await new.save(insert=True)
        bot.dispatch(f"{name}_create", new)
    for i in updated_ids:
        new = data_dict[i]
        old = attrs.evolve(getter(i))
        new_dict = new.to_dict()
        old_dict = old.to_dict()
        if no_compare is not None:
            for j in no_compare:
                new_dict.pop(j, None)
                old_dict.pop(j, None)
        if old is not None and new_dict != old_dict:
            old.update(new)
            await old.save()
            bot.dispatch(f"{name}_update", old, new)


class PnWDataTask(CommonTask):
    def __init__(self) -> None:
        super().__init__(interval=1800)

    async def before_task(self) -> None:
        next_run = utils.utcnow()
        # set next run equal to the next multiple of four minutes
        next_run = next_run.replace(
            minute=(next_run.minute // 5) * 5, second=0, microsecond=0
        ) + datetime.timedelta(minutes=5)
        # await utils.sleep_until(next_run.timestamp())

    async def task(self) -> None:
        print("RUNNING PNW TASK", flush=True)
        # treasures = [
        #     models.Treasure.from_data(i)
        #     for i in await pnwkit.async_treasure_query(
        #         {}, "name color continent bonus spawndate nation_id"
        #     )
        # ]
        # for i in treasures:
        #     treasure = cache.get_treasure(i.name)
        #     if treasure is None:
        #         cache.add_treasure(i)
        #         continue
        #     data = i.to_dict()
        #     if data != treasure.to_dict():
        #         old = attrs.evolve(treasure)
        #         treasure.update(i)
        #         bot.dispatch("treasure_update", old, treasure)
        # colors = [
        #     models.Color.from_data(i)
        #     for i in await pnwkit.async_color_query({}, "color bloc_name turn_bonus")
        # ]
        # for i in colors:
        #     color = cache.get_color(i.color)
        #     if color is None:
        #         cache.add_color(i)
        #         continue
        #     data = i.to_dict()
        #     if data != color.to_dict():
        #         old = attrs.evolve(color)
        #         color.update(i)
        #         bot.dispatch("color_update", old, color)
        # game_info = await pnwkit.async_game_info_query(
        #     {},
        #     {
        #         "radiation": "north_america south_america europe africa asia australia antarctica"
        #     },
        # )
        # radiation = models.Radiation.from_data(game_info["radiation"])
        # trades = {i.id: i for i in cache.trades if not i.accepted}
        await asyncio.wait(
            (
                handle_model_update(
                    "alliance",
                    models.Alliance,
                    kit.query(
                        "alliances",
                        {"first": 100},
                        "id name acronym score color date accept_members flag forum_link discord_link wiki_link",
                    ).paginate(
                        "alliances"
                    ),  # type: ignore
                    cache.alliances,
                    cache.add_alliance,
                    cache.get_alliance,
                    cache.remove_alliance,
                    ["estimated_resources"],
                ),
                handle_model_update(
                    "bankrec",
                    models.Bankrec,
                    kit.query(
                        "bankrecs",
                        {
                            "min_id": max(i.id for i in cache.bankrecs) + 1
                            if cache.bankrecs
                            else 0
                        },
                        "id date sender_id sender_type receiver_id receiver_type banker_id note money coal oil uranium iron bauxite lead gasoline munitions steel aluminum food tax_id",
                    ).paginate(
                        "bankrecs"
                    ),  # type: ignore
                    cache.bankrecs,
                    cache.add_bankrec,
                    cache.get_bankrec,
                    cache.remove_bankrec,
                ),
                handle_model_update(
                    "bounty",
                    models.Bounty,
                    kit.query(
                        "bounties",
                        {"first": 1000},
                        "id date nation_id amount type",
                    ).paginate(
                        "bounties"
                    ),  # type: ignore
                    cache.bounties,
                    cache.add_bounty,
                    cache.get_bounty,
                    cache.remove_bounty,
                ),
                handle_model_update(
                    "city",
                    models.City,
                    kit.query(
                        "cities",
                        {"first": 500},
                        "id nation_id name date infrastructure land powered coal_power oil_power nuclear_power wind_power coal_mine lead_mine bauxite_mine oil_well uranium_mine iron_mine farm oil_refinery steel_mill aluminum_refinery munitions_factory police_station hospital recycling_center subway supermarket bank shopping_mall stadium barracks factory hangar drydock nuke_date",
                    ).paginate(
                        "cities"
                    ),  # type: ignore
                    cache.cities,
                    cache.add_city,
                    cache.get_city,
                    cache.remove_city,
                ),
                handle_model_update(
                    "nation",
                    models.Nation,
                    kit.query(
                        "nations",
                        {"first": 500},
                        "id alliance_id alliance_position nation_name leader_name continent war_policy domestic_policy color num_cities score flag vacation_mode_turns beige_turns espionage_available last_active date soldiers tanks aircraft ships missiles nukes discord turns_since_last_city turns_since_last_project project_bits wars_won wars_lost tax_id alliance_seniority",
                    ).paginate(
                        "nations"
                    ),  # type: ignore
                    cache.nations,
                    cache.add_nation,
                    cache.get_nation,
                    cache.remove_nation,
                    ["estimated_resources"],
                ),
                # handle_model_update(
                #     "trade",
                #     models.Trade,
                #     pnwkit.async_trade_query(
                #         {"min_id": max(trades) + 1 if trades else 0},
                #         "id type date sid rid offer_resource offer_amount buy_or_sell accepted date_accepted",
                #         paginator=True,
                #     ),
                #     cache.trades,
                #     cache.add_trade,
                #     cache.get_trade,
                #     cache.remove_trade,
                # ),
                handle_model_update(
                    "treaty",
                    models.Treaty,
                    kit.query(
                        "treaties",
                        {},
                        "id date treaty_type treaty_url turns_left alliance1_id alliance2_id",
                    ).paginate(
                        "treaties"
                    ),  # type: ignore
                    cache.treaties,
                    cache.add_treaty,
                    cache.get_treaty,
                    cache.remove_treaty,
                ),
                # handle_model_update(
                #     "war_attack",
                #     models.WarAttack,
                #     pnwkit.async_warattack_query(
                #         {
                #             "min_id": max(i.id for i in cache.war_attacks) + 1
                #             if cache.war_attacks
                #             else 0
                #         },
                #         "id date attid defid type warid victor success attcas1 attcas2 defcas1 defcas2 cityid infradestroyed improvementslost moneystolen loot_info resistance_eliminated city_infra_before infra_destroyed_value att_mun_used def_mun_used att_gas_used def_gas_used aircraft_killed_by_tanks",
                #         paginator=True,
                #     ),
                #     cache.war_attacks,
                #     cache.add_war_attack,
                #     cache.get_war_attack,
                #     cache.remove_war_attack,
                # ),
                # handle_model_update(
                #     "war",
                #     models.War,
                #     pnwkit.async_war_query(
                #         "wars",
                #         {"days_ago": 7},
                #         "id date reason war_type attid att_alliance_id defid def_alliance_id groundcontrol airsuperiority navalblockade winner turnsleft attpoints defpoints att_resistance def_resistance attpeace defpeace att_fortify def_fortify att_gas_used def_gas_used att_mun_used def_mun_used att_alum_used def_alum_used att_steel_used def_steel_used att_infra_destroyed def_infra_destroyed att_money_looted def_money_looted att_soldiers_killed def_soldiers_killed att_tanks_killed def_tanks_killed att_aircraft_killed def_aircraft_killed att_ships_killed def_ships_killed att_missiles_used def_missiles_used att_nukes_used def_nukes_used att_infra_destroyed_value def_infra_destroyed_value",
                #         paginator=True,
                #     ),
                #     cache.wars,
                #     cache.add_war,
                #     cache.get_war,
                #     cache.remove_war,
                #     delete=False,
                # ),
            )
        )
