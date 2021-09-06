from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

import pnwkit

from ..query import query_city
from ..requests import get_city_build
from .base import Makeable
from .resources import Resources

if TYPE_CHECKING:
    from .nation import Nation

__all__ = ("City", "FullCity")


class City:
    data: Tuple[int, int, str, bool, float, float, float]
    id: int
    nation_id: int
    name: str
    capital: bool
    infrastructure: float
    maxinfra: float
    land: float

    def __init__(self, *, city_id=None, city_name=None, data) -> None:
        self.data = data
        self.id = self.data[0]
        self.nation_id = self.data[1]
        self.name = self.data[2]
        self.capital = self.data[3]
        self.infrastructure = self.data[4]
        self.maxinfra = self.data[5]
        self.land = self.data[6]

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

    def _update(self, *, city_id=None, city_name=None, data) -> City:
        self.data = data
        self.id = self.data[0]
        self.name = self.data[2]
        self.capital = self.data[3]
        self.infrastructure = self.data[4]
        self.maxinfra = self.data[5]
        self.land = self.data[6]
        return self

    async def _make_nation(self) -> None:
        from .nation import Nation

        try:
            self.nation = await Nation.fetch(self.nation_id)
        except IndexError:
            self.nation = None

    async def get_build(self) -> Dict[str, Any]:
        return await get_city_build(city_id=self.id)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id

    def __float__(self) -> Tuple[float, float]:
        return self.infrastructure, self.land


class FullCity(Makeable):
    data: Dict[str, Any]
    id: int
    name: Optional[str]
    nation_id: int
    capital: Optional[bool]
    age: Optional[int]
    infrastructure: float
    land: float
    population: int
    disease: float
    crime: float
    pollution: int
    commerce: float
    powered: bool
    coal_power: int
    oil_power: int
    nuclear_power: int
    wind_power: int
    coal_mines: int
    lead_mines: int
    bauxite_mines: int
    oil_wells: int
    uranium_mines: int
    iron_mines: int
    farms: int
    oil_refineries: int
    steel_mills: int
    aluminum_refineries: int
    munitions_factories: int
    police_stations: int
    hospitals: int
    recycling_centers: int
    subways: int
    supermarkets: int
    banks: int
    shopping_malls: int
    stadiums: int
    barracks: int
    factories: int
    hangars: int
    drydocks: int
    nation: Nation
    projects: pnwkit.data.Nation  # type: ignore

    __slots__ = (
        "data",
        "id",
        "name",
        "nation_id",
        "capital",
        "age",
        "infrastructure",
        "land",
        "population",
        "disease",
        "crime",
        "pollution",
        "commerce",
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

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.id = data["city_id"]
        self.name = data.get("name")
        self.nation_id = data["nation_id"]
        self.capital = data.get("capital")
        self.age = data.get("age")
        self.infrastructure = data["infrastructure"]
        self.land = data["land"]
        self.population = data["population"]
        self.disease = data["disease"]
        self.crime = data["crime"]
        self.pollution = data["pollution"]
        self.commerce = data["commerce"]
        self.powered = data["powered"]
        self.coal_power = data.get("coal_power", 0)
        self.oil_power = data.get("oil_power", 0)
        self.nuclear_power = data.get("nuclear_power", 0)
        self.wind_power = data.get("wind_power", 0)
        self.coal_mines = data.get("coal_mines", 0)
        self.lead_mines = data.get("lead_mines", 0)
        self.bauxite_mines = data.get("bauxite_mines", 0)
        self.oil_wells = data.get("oil_wells", 0)
        self.uranium_mines = data.get("uranium_mines", 0)
        self.iron_mines = data.get("iron_mines", 0)
        self.farms = data.get("farms", 0)
        self.oil_refineries = data.get("oil_refineries", 0)
        self.steel_mills = data.get("steel_mills", 0)
        self.aluminum_refineries = data.get("aluminum_refineries", 0)
        self.munitions_factories = data.get("materials_factories", 0)
        self.police_stations = data.get("police_stations", 0)
        self.hospitals = data.get("hospitals", 0)
        self.recycling_centers = data.get("recycling_centers", 0)
        self.subways = data.get("subways", 0)
        self.supermarkets = data.get("supermarkets", 0)
        self.banks = data.get("banks", 0)
        self.shopping_malls = data.get("shopping_malls", 0)
        self.stadiums = data.get("stadiums", 0)
        self.barracks = data.get("barracks", 0)
        self.factories = data.get("factories", 0)
        self.hangars = data.get("hangars", 0)
        self.drydocks = data.get("drydocks", 0)

    async def _make_projects(self) -> None:
        data = await pnwkit.async_nation_query(
            {"id": self.nation_id},
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
        )
        if TYPE_CHECKING:
            assert isinstance(data, tuple)
        self.projects = data[0]

    async def _make_nation(self) -> None:
        from .nation import Nation

        self.nation = await Nation.fetch(self.nation_id)

    async def calculate_income(self) -> Dict[str, Resources]:
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

    def calculate_net_money_income(self, income_modifier: float = 1) -> float:
        return (
            self.calculate_money_income(income_modifier)
            - (
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
            )
            - (
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
        )

    def calculate_net_food_income(self) -> float:
        return self.calculate_food_income() - (self.population / 1000)

    def calculate_net_coal_income(self) -> float:
        return (
            self.calculate_coal_income()
            - (self.coal_power * 1.2)
            - (
                (self.steel_mills * 3)
                * (1 + ((0.5 * (self.steel_mills - 1)) / (5 - 1)))
                * (1 + (0.36 * int(self.projects.ironw)))
            )
        )

    def calculate_net_oil_income(self) -> float:
        return (
            self.calculate_oil_income()
            - (self.oil_power * 1.2)
            - (
                (self.oil_refineries * 3)
                * (1 + ((0.5 * (self.oil_refineries - 1)) / (5 - 1)))
                * (1 + (0.36 * int(self.projects.egr)))
            )
        )

    def calculate_net_uranium_income(self) -> float:
        return self.calculate_uranium_income() - self.calculate_uranium_usage()

    def calculate_uranium_usage(self) -> float:
        amount = self.infrastructure // 1000
        if amount * 1000 < self.infrastructure:
            amount += 1
        amount = min(amount, self.nuclear_power * 2)
        return amount * 1.2

    def calculate_net_lead_income(self) -> float:
        return self.calculate_lead_income() - (
            (self.munitions_factories * 6)
            * (1 + ((0.5 * (self.munitions_factories - 1)) / (5 - 1)))
            * (1 + (0.34 * int(self.projects.armss)))
        )

    def calculate_net_iron_income(self) -> float:
        return self.calculate_iron_income() - (
            (self.steel_mills * 3)
            * (1 + ((0.5 * (self.steel_mills - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.ironw)))
        )

    def calculate_net_bauxite_income(self) -> float:
        return self.calculate_bauxite_income() - (
            (self.aluminum_refineries * 3)
            * (1 + ((0.5 * (self.aluminum_refineries - 1)) / (5 - 1)))
            * (1 + (0.36 * int(self.projects.bauxitew)))
        )

    def calculate_net_gasoline_income(self) -> float:
        return self.calculate_gasoline_income()

    def calculate_net_munitions_income(self) -> float:
        return self.calculate_munitions_income()

    def calculate_net_steel_income(self) -> float:
        return self.calculate_steel_income()

    def calculate_net_aluminum_income(self) -> float:
        return self.calculate_aluminum_income()
