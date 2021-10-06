from __future__ import annotations

import math
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

from src.errors.notfound import CityNotFoundError

from ...cache import cache
from ...errors import CityNotFoundError
from .base import Makeable
from .resources import Resources

__all__ = ("City", "FullCity")

if TYPE_CHECKING:
    from pnwkit.data import Nation as PnWKitNation

    from _typings import CityData

    from .nation import Nation


class City:
    __slots__ = (
        "id",
        "nation_id",
        "name",
        "capital",
        "infrastructure",
        "max_infra",
        "land",
    )

    def __init__(self, data: CityData) -> None:
        self.id: int = data["id"]
        self.nation_id: int = data["nation_id"]
        self.name: str = data["name"]
        self.capital: bool = data["capital"]
        self.infrastructure: float = data["infrastructure"]
        self.max_infra: float = data["max_infra"]
        self.land: float = data["land"]

    @classmethod
    async def fetch(cls, city_id: int, /) -> City:
        city = cache.get_city(city_id)
        if city:
            return city
        raise CityNotFoundError(city_id)

    def update(self, data: CityData, /) -> None:
        self.id: int = data["id"]
        self.nation_id: int = data["nation_id"]
        self.name: str = data["name"]
        self.capital: bool = data["capital"]
        self.infrastructure: float = data["infrastructure"]
        self.max_infra: float = data["max_infra"]
        self.land: float = data["land"]

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id

    def __float__(self) -> Tuple[float, float]:
        return self.infrastructure, self.land

    @cached_property
    def nation(self) -> Nation:
        return cache.get_nation(self.nation_id)  # type: ignore


class FullCity(Makeable):
    __slots__ = (
        "data",
        "id",
        "name",
        "nation_id",
        "age",
        "infrastructure",
        "land",
        "powered",
        "coal_power",
        "oil_power",
        "nuclear_power",
        "wind_power",
        "coal_mines",
        "lead_mines",
        "bauxite_mines",
        "oil_wells",
        "uranium_mines",
        "iron_mines",
        "farms",
        "oil_refineries",
        "steel_mills",
        "aluminum_refineries",
        "missiles_factories",
        "police_stations",
        "hospitals",
        "recycling_centers",
        "subways",
        "supermarkets",
        "banks",
        "shopping_malls",
        "stadiums",
        "barracks",
        "factories",
        "hangars",
        "drydocks",
    )

    def __init__(self, data: Dict[str, Any], nation: PnWKitNation) -> None:
        self.id: int = data.get("city_id") or data["id"]
        self.name: Optional[str] = data.get("name")
        self.nation_id: int = int(nation.id)
        self.age: int = (datetime.utcnow() - datetime.fromisoformat(data["date"])).days
        self.infrastructure: float = data["infrastructure"]
        self.land: float = data["land"]
        self.powered: bool = data["powered"]
        self.coal_power: int = data.get("coalpower", 0)
        self.oil_power: int = data.get("oilpower", 0)
        self.nuclear_power: int = data.get("nuclearpower", 0)
        self.wind_power: int = data.get("windpower", 0)
        self.coal_mines: int = data.get("coalmine", 0)
        self.lead_mines: int = data.get("leadmine", 0)
        self.bauxite_mines: int = data.get("bauxitemine", 0)
        self.oil_wells: int = data.get("oilwell", 0)
        self.uranium_mines: int = data.get("uramine", 0)
        self.iron_mines: int = data.get("ironmine", 0)
        self.farms: int = data.get("farm", 0)
        self.oil_refineries: int = data.get("gasrefinery", 0)
        self.steel_mills: int = data.get("steelmill", 0)
        self.aluminum_refineries: int = data.get("aluminumrefinery", 0)
        self.munitions_factories: int = data.get("munitionsfactory", 0)
        self.police_stations: int = data.get("policestation", 0)
        self.hospitals: int = data.get("hospital", 0)
        self.recycling_centers: int = data.get("recyclingcenter", 0)
        self.subways: int = data.get("subway", 0)
        self.supermarkets: int = data.get("supermarket", 0)
        self.banks: int = data.get("bank", 0)
        self.shopping_malls: int = data.get("mall", 0)
        self.stadiums: int = data.get("stadium", 0)
        self.barracks: int = data.get("barracks", 0)
        self.factories: int = data.get("factory", 0)
        self.hangars: int = data.get("airforcebase", 0)
        self.drydocks: int = data.get("drydock", 0)
        self.nation: Nation = cache.get_nation(self.nation_id)  # type: ignore
        self.projects: PnWKitNation = nation

    @cached_property
    def population(self) -> float:
        return (
            (
                (self.infrastructure * 100)
                - ((self.disease * 100 * self.infrastructure) / 10)
            )
            - max((self.crime / 10) * (100 * self.infrastructure) - 25, 0)
        ) * (1 + (math.log(self.age) if self.age else 0) / 15)

    @cached_property
    def disease(self) -> float:
        disease = (
            (((((self.infrastructure * 100 / self.land) ** 2) * 0.01) - 25) / 100)
            + (self.infrastructure * 100 / 100000)
            + (self.pollution * 0.05)
            - (self.hospitals * 2.5)
            - (self.hospitals * self.projects.clinical_research_center)
        )
        if disease < 0:
            return 0
        if disease > 100:
            return 100
        return disease

    @cached_property
    def crime(self) -> float:
        crime = (
            ((103 - self.commerce) ** 2 + (self.infrastructure * 100)) / (111111)
            - (self.police_stations * 2.5)
            - (self.police_stations * self.projects.specialized_police_training)
        )
        if crime < 0:
            return 0
        if crime > 100:
            return 100
        return crime

    @cached_property
    def pollution(self) -> float:
        return (
            self.coal_power * 8
            + self.oil_power * 6
            + self.coal_mines * 12
            + self.iron_mines * 12
            + self.bauxite_mines * 12
            + self.lead_mines * 12
            + self.uranium_mines * 20
            + self.farms * 2 * (1 - int(self.projects.green_tech) * 0.5)
            + self.oil_refineries * 32 * (1 - int(self.projects.green_tech) * 0.25)
            + self.steel_mills * 40 * (1 - int(self.projects.green_tech) * 0.25)
            + self.aluminum_refineries * 40 * (1 - int(self.projects.green_tech) * 0.25)
            + self.munitions_factories * 32 * (1 - int(self.projects.green_tech) * 0.25)
            + self.police_stations
            + self.hospitals * 4
            - self.recycling_centers * 70
            - self.recycling_centers * 5 * self.projects.recycling_initiative
            - self.subways * 45
            - self.subways * 25 * self.projects.green_tech
            + self.shopping_malls * 2
            + self.stadiums * 5
        )

    @cached_property
    def commerce(self) -> float:
        commerce = (
            self.supermarkets * 3
            + self.banks * 5
            + self.shopping_malls * 9
            + self.stadiums * 12
            + self.projects.telecom_satellite * 2
        )
        if self.projects.telecom_satellite:
            return commerce
        if self.projects.itc:
            return min(commerce, 115)
        return min(commerce, 100)

    def calculate_income(self) -> Dict[str, Resources]:
        """
        Income is per day.
        """
        return {
            "gross_income": Resources(
                money=self.calculate_money_income(),
                food=self.calculate_food_income(),
                coal=self.calculate_coal_income(),
                oil=self.calculate_oil_income(),
                uranium=self.calculate_uranium_income(),
                lead=self.calculate_lead_income(),
                iron=self.calculate_iron_income(),
                bauxite=self.calculate_bauxite_income(),
                gasoline=self.calculate_gasoline_income(),
                munitions=self.calculate_munitions_income(),
                steel=self.calculate_steel_income(),
                aluminum=self.calculate_aluminum_income(),
            ),
            "net_income": Resources(
                money=self.calculate_net_money_income(),
                food=self.calculate_net_food_income(),
                coal=self.calculate_net_coal_income(),
                oil=self.calculate_net_oil_income(),
                uranium=self.calculate_net_uranium_income(),
                lead=self.calculate_net_lead_income(),
                iron=self.calculate_net_iron_income(),
                bauxite=self.calculate_net_bauxite_income(),
                gasoline=self.calculate_net_gasoline_income(),
                munitions=self.calculate_net_munitions_income(),
                steel=self.calculate_net_steel_income(),
                aluminum=self.calculate_net_aluminum_income(),
            ),
            "upkeep": Resources(
                money=self.calculate_money_upkeep(),
                food=self.calculate_food_upkeep(),
                coal=self.calculate_coal_upkeep(),
                oil=self.calculate_oil_upkeep(),
                uranium=self.calculate_uranium_upkeep(),
                lead=self.calculate_lead_upkeep(),
                iron=self.calculate_iron_upkeep(),
                bauxite=self.calculate_bauxite_upkeep(),
            ),
        }

    def calculate_money_income(self, income_modifier: float = 1) -> float:
        if not self.powered:
            return 0.725 * self.population
        if self.nation.domestic_policy == "Open Markets":
            return (((self.commerce / 50) * 0.725) + 0.725) * self.population * 1.01
        return (
            (((self.commerce / 50) * 0.725) + 0.725) * self.population * income_modifier
        )

    def calculate_food_income(self) -> float:
        if not self.farms:
            return 0
        return (
            (self.land / (500 - (int(self.projects.massirr) * 100)))
            * self.farms
            * (1 + ((0.5 * (self.farms - 1)) / (10 - 1)))
            * 12
        )

    def calculate_coal_income(self) -> float:
        if not self.coal_mines:
            return 0
        return 3 * self.coal_mines * (1 + ((0.5 * (self.coal_mines - 1)) / (10 - 1)))

    def calculate_oil_income(self) -> float:
        if not self.oil_wells:
            return 0
        return 3 * self.oil_wells * (1 + ((0.5 * (self.oil_wells - 1)) / (10 - 1)))

    def calculate_uranium_income(self) -> float:
        if not self.uranium_mines:
            return 0
        return (
            3
            * self.uranium_mines
            * (1 + ((0.5 * (self.uranium_mines - 1)) / (5 - 1)))
            * (1 + int(self.projects.uap))
        )

    def calculate_lead_income(self) -> float:
        if not self.lead_mines:
            return 0
        return 3 * self.lead_mines * (1 + ((0.5 * (self.lead_mines - 1)) / (10 - 1)))

    def calculate_iron_income(self) -> float:
        if not self.iron_mines:
            return 0
        return 3 * self.iron_mines * (1 + ((0.5 * (self.iron_mines - 1)) / (10 - 1)))

    def calculate_bauxite_income(self) -> float:
        if not self.bauxite_mines:
            return 0
        return (
            3 * self.bauxite_mines * (1 + ((0.5 * (self.bauxite_mines - 1)) / (10 - 1)))
        )

    def calculate_gasoline_income(self) -> float:
        if not self.oil_refineries or not self.powered:
            return 0
        return (
            6
            * self.oil_refineries
            * (1 + ((0.5 * (self.oil_refineries - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.egr)))
        )

    def calculate_munitions_income(self) -> float:
        if not self.munitions_factories or not self.powered:
            return 0
        return (
            18
            * self.munitions_factories
            * (1 + ((0.5 * (self.munitions_factories - 1)) / (5 - 1)))
            * (1 + (0.34 * int(self.projects.armss)))
        )

    def calculate_steel_income(self) -> float:
        if not self.steel_mills or not self.powered:
            return 0
        return (
            9
            * self.steel_mills
            * (1 + ((0.5 * (self.steel_mills - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.ironw)))
        )

    def calculate_aluminum_income(self) -> float:
        if not self.aluminum_refineries or not self.powered:
            return 0
        return (
            9
            * self.aluminum_refineries
            * (1 + ((0.5 * (self.aluminum_refineries - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.bauxitew)))
        )

    def calculate_money_upkeep(self):
        return (
            (self.coal_power * 1200)
            + (self.oil_power * 1800)
            + (self.nuclear_power * 10500)
            + (self.wind_power * 500)
            + (self.coal_mines * 400)
            + (self.oil_wells * 600)
            + (self.iron_mines * 1600)
            + (self.bauxite_mines * 1600)
            + (self.lead_mines * 1500)
            + (self.uranium_mines * 5000)
            + (self.farms * 300)
        ) + (
            (
                (self.oil_refineries * 4000)
                + (self.steel_mills * 4000)
                + (self.aluminum_refineries * 2500)
                + (self.munitions_factories * 3500)
                + (self.police_stations * 750)
                + (self.hospitals * 1000)
                + (self.recycling_centers * 2500)
                + (self.subways * 3250)
                + (self.supermarkets * 600)
                + (self.banks * 1800)
                + (self.shopping_malls * 5400)
                + (self.stadiums * 12150)
            )
            if self.powered
            else 0
        )

    def calculate_food_upkeep(self):
        return self.population / 1000

    def calculate_coal_upkeep(self):
        return (self.coal_power * 1.2) + (
            (self.steel_mills * 3)
            * (1 + ((0.5 * (self.steel_mills - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.ironw)))
        )

    def calculate_oil_upkeep(self):
        return (self.oil_power * 1.2) + (
            (self.oil_refineries * 3)
            * (1 + ((0.5 * (self.oil_refineries - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.egr)))
        )

    def calculate_uranium_upkeep(self) -> float:
        amount = self.infrastructure // 1000
        if amount * 1000 < self.infrastructure:
            amount += 1
        amount = min(amount, self.nuclear_power * 2)
        return amount * 1.2

    def calculate_lead_upkeep(self) -> float:
        return (
            (self.munitions_factories * 6)
            * (1 + ((0.5 * (self.munitions_factories - 1)) / (5 - 1)))
            * (1 + (0.34 * int(self.projects.armss)))
        )

    def calculate_iron_upkeep(self) -> float:
        return (
            (self.steel_mills * 3)
            * (1 + ((0.5 * (self.steel_mills - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.ironw)))
        )

    def calculate_bauxite_upkeep(self) -> float:
        return (
            (self.aluminum_refineries * 3)
            * (1 + ((0.5 * (self.aluminum_refineries - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.bauxitew)))
        )

    def calculate_net_money_income(self, income_modifier: float = 1) -> float:
        return (
            self.calculate_money_income(income_modifier) - self.calculate_money_upkeep()
        )

    def calculate_net_food_income(self) -> float:
        return self.calculate_food_income() - self.calculate_food_upkeep()

    def calculate_net_coal_income(self) -> float:
        return self.calculate_coal_income() - self.calculate_coal_upkeep()

    def calculate_net_oil_income(self) -> float:
        return self.calculate_oil_income() - self.calculate_oil_upkeep()

    def calculate_net_uranium_income(self) -> float:
        return self.calculate_uranium_income() - self.calculate_uranium_upkeep()

    def calculate_net_lead_income(self) -> float:
        return self.calculate_lead_income() - self.calculate_lead_upkeep()

    def calculate_net_iron_income(self) -> float:
        return self.calculate_iron_income() - self.calculate_iron_upkeep()

    def calculate_net_bauxite_income(self) -> float:
        return self.calculate_bauxite_income() - self.calculate_bauxite_upkeep()

    calculate_net_gasoline_income = calculate_gasoline_income
    calculate_net_munitions_income = calculate_munitions_income
    calculate_net_steel_income = calculate_steel_income
    calculate_net_aluminum_income = calculate_aluminum_income
