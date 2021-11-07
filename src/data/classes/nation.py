from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, List, Optional

import aiohttp
import discord
import pnwkit
from bs4 import BeautifulSoup
from discord.utils import MISSING

from ...cache import cache
from ...data.db import execute_read_query
from ...errors import NationNotFoundError
from ...find import search_nation
from ...funcs import utils
from ...ref import RiftContext, bot
from .base import Makeable

__all__ = ("Nation",)

if TYPE_CHECKING:
    from pnwkit.data import Nation as PnWKitNation

    from _typings import Field, NationData, RevenueDict

    from .alliance import Alliance
    from .city import City
    from .condition import Condition
    from .target import Target
    from .trade import TradePrices
    from .war import Attack, War


class Nation(Makeable):
    __slots__ = (
        "id",
        "name",
        "leader",
        "continent",
        "war_policy",
        "domestic_policy",
        "color",
        "alliance_id",
        "alliance_position",
        "cities",
        "offensive_wars",
        "defensive_wars",
        "score",
        "v_mode",
        "v_mode_turns",
        "beige_turns",
        "last_active",
        "founded",
        "soldiers",
        "tanks",
        "aircraft",
        "ships",
        "missiles",
        "nukes",
    )

    def __init__(self, data: NationData):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.leader: str = data["leader"]
        self.continent: str = utils.get_continent(data["continent"])
        self.war_policy: str = utils.get_war_policy(data["war_policy"])
        self.domestic_policy: str = utils.get_domestic_policy(data["domestic_policy"])
        self.color: str = utils.get_color(data["color"])
        self.alliance_id: int = data["alliance_id"]
        self.alliance_position: str = utils.get_alliance_position(
            data["alliance_position"]
        )
        self.cities: int = data["cities"]
        self.offensive_wars: int = data["offensive_wars"]
        self.defensive_wars: int = data["defensive_wars"]
        self.score: float = data["score"]
        self.v_mode: bool = data["v_mode"]
        self.v_mode_turns: int = data["v_mode_turns"]
        self.beige_turns: int = data["beige_turns"]
        self.last_active: str = data["last_active"]
        self.founded: str = data["founded"]
        self.soldiers: int = data["soldiers"]
        self.tanks: int = data["tanks"]
        self.aircraft: int = data["aircraft"]
        self.ships: int = data["ships"]
        self.missiles: int = data["missiles"]
        self.nukes: int = data["nukes"]

    @classmethod
    async def convert(
        cls, ctx: RiftContext, search: Any, advanced: bool = True
    ) -> Nation:
        return await search_nation(ctx, search, advanced)

    @classmethod
    async def fetch(cls, nation_id: int) -> Nation:
        nation = cache.get_nation(nation_id)
        if nation:
            return nation
        raise NationNotFoundError(nation_id)

    def update(self, data: NationData):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.leader: str = data["leader"]
        self.continent: str = utils.get_continent(data["continent"])
        self.war_policy: str = utils.get_war_policy(data["war_policy"])
        self.domestic_policy: str = utils.get_domestic_policy(data["domestic_policy"])
        self.color: str = utils.get_color(data["color"])
        self.alliance_id: int = data["alliance_id"]
        self.alliance_position: str = utils.get_alliance_position(
            data["alliance_position"]
        )
        self.cities: int = data["cities"]
        self.offensive_wars: int = data["offensive_wars"]
        self.defensive_wars: int = data["defensive_wars"]
        self.score: float = data["score"]
        self.v_mode: bool = data["v_mode"]
        self.v_mode_turns: int = data["v_mode_turns"]
        self.beige_turns: int = data["beige_turns"]
        self.last_active: str = data["last_active"]
        self.founded: str = data["founded"]
        self.soldiers: int = data["soldiers"]
        self.tanks: int = data["tanks"]
        self.aircraft: int = data["aircraft"]
        self.ships: int = data["ships"]
        self.missiles: int = data["missiles"]
        self.nukes: int = data["nukes"]

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.id

    def __float__(self) -> float:
        return self.score

    def __len__(self) -> int:
        return self.cities

    def __bool__(self) -> bool:
        return True

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    @property
    def user(self) -> Optional[discord.User]:
        link = cache.get_user(self.id)
        if link is None:
            return
        return bot.get_user(link["user_id"])

    @property
    def partial_cities(self) -> List[City]:
        return [i for i in cache.cities if i.nation_id == self.id]

    async def send_message(
        self, *, subject: Optional[str] = None, content: Optional[str] = None
    ):
        from ...ref import bot

        message_data = {
            "newconversation": "true",
            "receiver": self.leader,
            "subject": subject,
            "body": content,
            "sndmsg": "Send Message",
        }
        async with bot.pnw_session.post(
            "https://politicsandwar.com/inbox/message", data=message_data, timeout=30.0
        ) as response:
            return "successfully" in (await response.text()).lower()

    def get_militarization(self):
        militarization = {
            "soldiers": self.soldiers / (self.cities * 15000),
            "tanks": self.tanks / (self.cities * 1250),
            "aircraft": self.aircraft / (self.cities * 75),
            "ships": self.ships / (self.cities * 15),
        }
        militarization["total"] = sum(militarization.values()) / 4
        return militarization

    def get_average_infrastructure(self):
        return sum(i.infrastructure for i in self.partial_cities) / self.cities

    avg_infra = get_average_infrastructure

    async def get_discord_page_username(self):
        async with aiohttp.request(
            "GET", f"https://politicsandwar.com/nation/id={self.id}"
        ) as response:
            return [
                i.contents[1].text  # type: ignore
                for i in BeautifulSoup(await response.text(), "html.parser").find_all(
                    "tr", class_="notranslate"
                )
                if any("Discord Username:" in str(j) for j in i.contents)  # type: ignore
            ][0]

    def get_info_embed(self, ctx: RiftContext) -> discord.Embed:
        from ...funcs import get_embed_author_guild, get_embed_author_member

        fields: List[Field] = [
            {"name": "Nation ID", "value": self.id},
            {"name": "Nation Name", "value": self.name},
            {"name": "Leader Name", "value": self.leader},
            {"name": "War Policy", "value": self.war_policy},
            {"name": "Domestic Policy", "value": self.domestic_policy},
            {"name": "Continent", "value": self.continent},
            {
                "name": "Color",
                "value": self.color
                if self.color != "Beige"
                else f"Beige ({self.beige_turns:,} Turns)",
            },
            {
                "name": "Alliance",
                "value": f"[{repr(self.alliance)}](https://politicsandwar.com/alliance/id={self.alliance.id})"
                if self.alliance is not None
                else "None",
            },
            {"name": "Alliance Position", "value": self.alliance_position},
            {
                "name": "Cities",
                "value": f"[{self.cities}](https://politicsandwar.com/?id=62&n={'+'.join(self.name.split(' '))})",
            },
            {"name": "Score", "value": f"{self.score:,.2f}"},
            {
                "name": "Vacation Mode",
                "value": f"True ({self.v_mode_turns:,} Turns)"
                if self.v_mode
                else "False",
            },
            {
                "name": "Soldiers",
                "value": f"{self.soldiers:,}/{self.cities *15000:,}",
            },
            {
                "name": "Tanks",
                "value": f"{self.tanks:,}/{self.cities * 1250:,}",
            },
            {
                "name": "Aircraft",
                "value": f"{self.aircraft:,}/{self.cities * 75:,}",
            },
            {
                "name": "Ships",
                "value": f"{self.ships:,}/{self.cities * 15:,}",
            },
            {"name": "Missiles", "value": f"{self.missiles:,}"},
            {"name": "Nukes", "value": f"{self.nukes:,}"},
            {
                "name": "Offensive Wars",
                "value": f"[{self.offensive_wars}](https://politicsandwar.com/nation/id={self.id}&display=war)",
            },
            {
                "name": "Defensive Wars",
                "value": f"[{self.defensive_wars}](https://politicsandwar.com/nation/id={self.id}&display=war)",
            },
            {"name": "Average Infrastructure", "value": f"{self.avg_infra():,.2f}"},
            {
                "name": "Actions",
                "value": f"[\U0001f4e7](https://politicsandwar.com/inbox/message/receiver={'+'.join(self.leader.split(' '))})"
                f"[\U0001f4e4](https://politicsandwar.com/nation/trade/create/nation={'+'.join(self.name.split(' '))})"
                f"[\U000026d4](https://politicsandwar.com/index.php?id=68&name={'+'.join(self.name.split(' '))}&type=n)"
                f"[\U00002694](https://politicsandwar.com/nation/war/declare/id={self.id})"
                f"[\U0001f575](https://politicsandwar.com/nation/espionage/eid={self.id})",
            },
        ]
        return (
            get_embed_author_member(
                self.user,
                f"[Nation Page](https://politicsandwar.com/nation/id={self.id})",
                timestamp=datetime.datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
                color=discord.Color.blue(),
            )
            if self.user is not None
            else get_embed_author_member(
                ctx.author,
                f"[Nation Page](https://politicsandwar.com/nation/id={self.id})",
                timestamp=datetime.datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
                color=discord.Color.blue(),
            )
            if ctx.guild is None
            else get_embed_author_guild(
                ctx.guild,
                f"[Nation Page](https://politicsandwar.com/nation/id={self.id})",
                timestamp=datetime.datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
                color=discord.Color.blue(),
            )
        )

    async def calculate_revenue(
        self,
        prices: Optional[TradePrices] = None,
        data: Optional[PnWKitNation] = None,
        fetch_spies: bool = False,
    ) -> RevenueDict:
        # sourcery no-metrics
        from ...funcs import calculate_spies
        from .city import FullCity
        from .color import Color
        from .resources import Resources

        spies = await calculate_spies(self) if fetch_spies else 0
        prices = prices or cache.prices
        if not data:
            raw_data = await pnwkit.async_nation_query(  # type: ignore
                {"id": self.id},
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
            if TYPE_CHECKING:
                assert isinstance(raw_data, tuple)
            data = raw_data[0]
        cities = [FullCity(i, data) for i in data.cities]  # type: ignore
        revenues = [i.calculate_income() for i in cities]
        revenue: RevenueDict = {  # type: ignore
            "gross_income": sum(
                (i["gross_income"] for i in revenues[1:]), revenues[0]["gross_income"]
            ),
            "net_income": sum(
                (i["net_income"] for i in revenues[1:]), revenues[0]["net_income"]
            ),
            "upkeep": sum((i["upkeep"] for i in revenues[1:]), revenues[0]["upkeep"]),
        }
        color = await Color.fetch(self.color.lower())
        bonus = color.bonus * 12
        if self.cities <= 10:
            revenue["new_player_bonus"] = revenue["gross_income"].money * 1.1 - (
                0.1 * self.cities
            )
            revenue["gross_income"].money *= 2.1 - (0.1 * self.cities)
            revenue["net_income"].money = sum(
                i.calculate_net_money_income(2.1 - (0.1 * self.cities)) for i in cities
            )
        revenue["gross_income"].money += bonus
        revenue["net_income"].money += bonus
        if self.offensive_wars or self.defensive_wars:
            revenue["net_income"].money -= (
                (1.88 * (self.soldiers / 500))
                + (75 * self.tanks)
                + (750 * self.aircraft)
                + (5625 * self.ships)
                + (2400 * spies)
                + (31500 * self.missiles)
                + (52500 * self.nukes)
            )
            revenue["net_income"].food -= self.soldiers / 500
            revenue["upkeep"].food += self.soldiers / 500
            revenue["upkeep"].money += (
                (1.88 * (self.soldiers / 500))
                + (75 * self.tanks)
                + (750 * self.aircraft)
                + (5625 * self.ships)
                + (2400 * spies)
                + (31500 * self.missiles)
                + (52500 * self.nukes)
            )
        else:
            revenue["net_income"].money -= (
                (1.25 * (self.soldiers / 750))
                + (50 * self.tanks)
                + (500 * self.aircraft)
                + (3750 * self.ships)
                + (2400 * spies)
                + (21000 * self.missiles)
                + (35000 * self.nukes)
            )
            revenue["net_income"].food -= self.soldiers / 750
            revenue["upkeep"].money += (
                (1.25 * (self.soldiers / 750))
                + (50 * self.tanks)
                + (500 * self.aircraft)
                + (3750 * self.ships)
                + (2400 * spies)
                + (21000 * self.missiles)
                + (35000 * self.nukes)
            )
            revenue["upkeep"].food += self.soldiers / 750
        revenue["gross_total"] = Resources(
            **{
                key: value * getattr(prices, key).lowest_sell.price
                for key, value in revenue["gross_income"].to_dict().items()
                if key != "money"
            }
        )
        revenue["net_total"] = Resources(
            **{
                key: value * getattr(prices, key).lowest_sell.price
                for key, value in revenue["net_income"].to_dict().items()
                if key != "money"
            }
        )
        revenue["upkeep_total"] = Resources(
            **{
                key: value * getattr(prices, key).lowest_sell.price
                for key, value in revenue["upkeep"].to_dict().items()
                if key != "money"
            }
        )
        revenue["trade_bonus"] = bonus
        return revenue

    async def fetch_projects(self) -> PnWKitNation:
        return (
            await pnwkit.async_nation_query(  # type: ignore
                {"id": self.id},
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
            )
        )[0]

    async def calculate_spies(self) -> int:
        from ...funcs import calculate_spies

        return await calculate_spies(self)

    async def find_targets(
        self,
        condition: Condition = MISSING,
        wars: Optional[List[War]] = None,
        attacks: Optional[List[Attack]] = None,
        /,
        loot: bool = False,
    ) -> List[Target]:
        from ...funcs import bulk_fetch_nation_revenues
        from .target import Target
        from .war import Attack, War

        valid = [i for i in cache.nations if self.check_war_range(i) and i is not self]
        if condition is not MISSING:
            valid = await condition.reduce(*valid)
        if loot:
            dt = datetime.datetime.utcnow()
            revenue_valid = [
                i
                for i in valid
                if (t := cache.get_target(i.id)) is None or t and t.turn_passed(dt)
            ]
            revenues = await bulk_fetch_nation_revenues(revenue_valid)
        else:
            revenues = {}
        targets: List[Target] = []
        valid_nation_ids = {i.id for i in valid}
        days_ago = str(datetime.datetime.utcnow() - datetime.timedelta(days=14))
        if wars is None:
            wars = [
                War(i)
                for i in await execute_read_query(
                    "SELECT * FROM wars WHERE date >= $1;",
                    days_ago,
                )
            ]
        if attacks is None:
            attacks = [
                Attack(i)
                for i in await execute_read_query(
                    "SELECT * FROM attacks WHERE date >= $1;",
                    days_ago,
                )
            ]
        wars = wars and [j for j in wars if j.attacker_id in valid_nation_ids]
        if wars:
            valid_war_ids = {i.id for i in wars}
            attacks = attacks and [j for j in attacks if j.war_id in valid_war_ids]
        for i in valid:
            wars_ = wars and [
                j for j in wars if j.attacker_id == i.id and j.defender_id == i.id
            ]
            if wars_ is not None:
                war_ids = {j.id for j in wars_}
                attacks_ = attacks and [j for j in attacks if j.war_id in war_ids]
            else:
                attacks_ = None
            try:
                targets.append(
                    await Target.create(
                        i,
                        revenues.get(i.id, {"net_income": None})["net_income"],
                        wars_,
                        attacks_,
                        loot=loot,
                    )
                )
            # nation does not exist but is still in cache
            except IndexError:
                continue
        return targets

    async def fetch_last_wars(self) -> List[War]:
        from .war import War

        return [
            War(i)
            for i in (
                await execute_read_query(
                    "SELECT * FROM wars WHERE (attacker_id = $1 or defender_id = $1) AND winner != 0 ORDER BY date LIMIT 10;",
                    self.id,
                )
            )
        ]

    def check_war_range(self, nation: Nation, /) -> bool:
        return self.score * 1.75 > nation.score > self.score * 0.75
