from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Dict, List

import pnwkit

from ..cache import cache

__all__ = ("bulk_fetch_nation_revenues",)

if TYPE_CHECKING:
    from _typings import RevenueDict

    from ..data.classes import Nation


async def bulk_fetch_nation_revenues(nations: List[Nation]) -> Dict[int, RevenueDict]:
    revenues: Dict[int, RevenueDict] = {}
    nations_ = {i.id: i for i in nations}
    prices = cache.get_prices()
    ids: List[int] = []
    cities = 0
    num = len(nations) - 1
    for index, nation in enumerate(nations):
        ids.append(nation.id)
        cities += nation.cities
        if cities >= 6000 or len(ids) >= 400 or index == num:
            s = time.perf_counter()
            raw_data = await pnwkit.async_nation_query(  # type: ignore
                {"id": ids, "first": 500},
                "id",
                "ironw",
                "bauxitew",
                "armss",
                "egr",
                "massirr",
                "itc",
                "mlp",
                "nrf",
                "irond",
                "vds",
                "cia",
                "cfce",
                "propb",
                "uap",
                "city_planning",
                "adv_city_planning",
                "space_program",
                "spy_satellite",
                "moon_landing",
                "pirate_economy",
                "recycling_initiative",
                "telecom_satellite",
                "green_tech",
                "arable_land_agency",
                "clinical_research_center",
                "specialized_police_training",
                "adv_engineering_corps",
                {
                    "cities": (
                        "id",
                        "name",
                        "date",
                        "infrastructure",
                        "land",
                        "powered",
                        "oilpower",
                        "windpower",
                        "coalpower",
                        "nuclearpower",
                        "coalmine",
                        "oilwell",
                        "uramine",
                        "barracks",
                        "farm",
                        "policestation",
                        "hospital",
                        "recyclingcenter",
                        "subway",
                        "supermarket",
                        "bank",
                        "mall",
                        "stadium",
                        "leadmine",
                        "ironmine",
                        "bauxitemine",
                        "gasrefinery",
                        "aluminumrefinery",
                        "steelmill",
                        "munitionsfactory",
                        "factory",
                        "airforcebase",
                        "drydock",
                    )
                },
            )
            e = time.perf_counter()
            for i in raw_data:
                revenues[int(i.id)] = await nations_[int(i.id)].calculate_revenue(
                    prices, i
                )
            if e - s < 1.1:
                await asyncio.sleep(1.1 - (e - s))
            cities = 0
            ids = []
    return revenues
