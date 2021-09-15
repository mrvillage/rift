from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union
from urllib.parse import quote

import aiohttp
import discord
import pnwkit
from bs4 import BeautifulSoup
from discord.ext import commands

from ...cache import cache
from ...data.get import get_link_nation
from ...errors import NationNotFoundError
from ...find import search_nation
from ...funcs import utils
from ..query import query_nation, query_nation_cities
from .base import Makeable

__all__ = ("Nation",)

if TYPE_CHECKING:
    from pnwkit.data import Nation as PnWKitNation

    from typings import NationData

    from .alliance import Alliance
    from .city import City
    from .resources import Resources
    from .trade import TradePrices


class Nation(Makeable):
    __slots__ = (
        "data",
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
    async def convert(cls, ctx, search):
        return await search_nation(ctx, search)

    @classmethod
    async def fetch(cls, nation_id: int) -> Nation:
        nation = cache.get_nation(nation_id)
        if nation:
            return nation
        raise NationNotFoundError(nation_id)

    def _update(self, data: NationData):
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
        ...

    @property
    def partial_cities(self) -> List[City]:
        return [i for i in cache.cities if i.nation_id == self.id]

    async def send_message(self, *, subject: str = None, content: str = None):
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

    async def get_info_embed(self, ctx: commands.Context) -> discord.Embed:
        from ...funcs import get_embed_author_guild, get_embed_author_member

        await self.make_attrs("alliance", "user", "partial_cities")
        fields = [
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
                "value": f'[{repr(self.alliance)}](https://politicsandwar.com/alliance/id={self.alliance.id} "https://politicsandwar.com/alliance/id={self.alliance.id}")'
                if self.alliance is not None
                else "None",
            },
            {"name": "Alliance Position", "value": self.alliance_position},
            {
                "name": "Cities",
                "value": f"[{self.cities}](https://politicsandwar.com/?id=62&n={'+'.join(self.name.split(' '))} \"https://politicsandwar.com/?id=62&n={'+'.join(self.name.split(' '))}\")",
            },
            {"name": "Score", "value": f"{self.score:,.2f}"},
            {
                "name": "Vacation Mode",
                "value": f"True ({self.v_mode_turns:,} Turns)"
                if self.v_mode
                else "False",
            },
            {"name": "Soldiers", "value": f"{self.soldiers:,}"},
            {"name": "Tanks", "value": f"{self.tanks:,}"},
            {"name": "Aircraft", "value": f"{self.aircraft:,}"},
            {"name": "Ships", "value": f"{self.ships:,}"},
            {"name": "Missiles", "value": f"{self.missiles:,}"},
            {"name": "Nukes", "value": f"{self.nukes:,}"},
            {
                "name": "Offensive Wars",
                "value": f'[{self.offensive_wars}](https://politicsandwar.com/nation/id={self.id}&display=war "https://politicsandwar.com/nation/id={self.id}&display=war")',
            },
            {
                "name": "Defensive Wars",
                "value": f'[{self.defensive_wars}](https://politicsandwar.com/nation/id={self.id}&display=war "https://politicsandwar.com/nation/id={self.id}&display=war")',
            },
            {"name": "Average Infrastructure", "value": f"{self.avg_infra():,.2f}"},
            {
                "name": "Actions",
                "value": f"[\U0001f4e7](https://politicsandwar.com/inbox/message/receiver={'+'.join(self.leader.split(' '))} \"https://politicsandwar.com/inbox/message/receiver={'+'.join(self.leader.split(' '))}\") "
                f"[\U0001f4e4](https://politicsandwar.com/nation/trade/create/nation={'+'.join(self.name.split(' '))} \"https://politicsandwar.com/nation/trade/create/nation={'+'.join(self.name.split(' '))}\") "
                f"[\U000026d4](https://politicsandwar.com/index.php?id=68&name={'+'.join(self.name.split(' '))}&type=n \"https://politicsandwar.com/index.php?id=68&name={'+'.join(self.name.split(' '))}&type=n\") "
                f'[\U00002694](https://politicsandwar.com/nation/war/declare/id={self.id} "https://politicsandwar.com/nation/war/declare/id={self.id}") '
                f'[\U0001f575](https://politicsandwar.com/nation/espionage/eid={self.id} "https://politicsandwar.com/nation/espionage/eid={self.id}") ',
            },
        ]
        return (
            get_embed_author_member(
                ctx.author,
                f'[Nation Page](https://politicsandwar.com/nation/id={self.id} "https://politicsandwar.com/nation/id={self.id}")',
                timestamp=datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
                color=discord.Color.blue(),
            )
            if ctx.guild is None
            else get_embed_author_guild(
                ctx.guild,
                f'[Nation Page](https://politicsandwar.com/nation/id={self.id} "https://politicsandwar.com/nation/id={self.id}")',
                timestamp=datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
                color=discord.Color.blue(),
            )
            if self.user is None
            else get_embed_author_member(
                self.user,
                f'[Nation Page](https://politicsandwar.com/nation/id={self.id} "https://politicsandwar.com/nation/id={self.id}")',
                timestamp=datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
                color=discord.Color.blue(),
            )
        )

    async def scrape_city_manager(self) -> Sequence[Dict[str, Any]]:
        from ...funcs import get_trade_prices
        from ...funcs.utils import convert_link

        async with aiohttp.request(
            "GET", f"https://politicsandwar.com/city/manager/n={quote(self.name)}"
        ) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
        table = soup.find_all(class_="nationtable")[1]
        rows = table.find_all("tr")  # type: ignore
        ids = [
            int(await convert_link(i.contents[0].attrs["href"]))
            for i in rows[0].contents[2:]
        ]
        del rows[:2]
        items = [
            (row.contents[0].contents[0].contents[0].lower().replace(" ", "_"), row)
            for row in rows
        ]
        for row in rows:
            del row.contents[:2]
        values = {}
        for key, row in items:
            values[key] = []
            for i in row.contents:
                val = i.contents[0]
                if val == "Yes":
                    values[key].append(True)
                elif val == "No":
                    values[key].append(False)
                elif "%" in val:
                    values[key].append(float(val.replace("%", "")))
                elif "." in val:
                    values[key].append(float(val.replace(",", "")))
                elif "," in val:
                    values[key].append(int(val.replace(",", "")))
                else:
                    values[key].append(int(val))
        cities = []
        for index, id in enumerate(ids):
            city = {"city_id": id, "nation_id": self.id}
            for key, value in list(values.items()):
                city[key] = value[index]
            cities.append(city)
        return cities

    async def calculate_revenue(
        self,
        prices: TradePrices = None,
        data: PnWKitNation = None,
        fetch_spies: bool = False,
    ) -> Dict[str, Union[Resources, Dict[str, float], int, float]]:
        # sourcery no-metrics
        from ...funcs import calculate_spies, get_trade_prices
        from .city import FullCity
        from .color import Color
        from .resources import Resources

        revenue: Dict[str, Union[Resources, Dict[str, float], int, float]]
        spies = await calculate_spies(self) if fetch_spies else 0
        prices = prices or await get_trade_prices()
        if not data:
            raw_data = await pnwkit.async_nation_query(
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
        revenue = {
            "gross_income": sum(
                (i["gross_income"] for i in revenues[1:]), revenues[0]["gross_income"]
            ),
            "net_income": sum(
                (i["net_income"] for i in revenues[1:]), revenues[0]["net_income"]
            ),
        }
        color = await Color.fetch(self.color.lower())
        bonus = color.bonus * 12
        if TYPE_CHECKING:
            assert isinstance(revenue["gross_income"], Resources) and isinstance(
                revenue["net_income"], Resources
            )
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
        revenue["gross_total"] = Resources(
            **{
                key: value * getattr(prices, key).lowest_sell.price
                for key, value in revenue["gross_income"].__dict__.items()
                if key != "money"
            }
        )
        revenue["net_total"] = Resources(
            **{
                key: value * getattr(prices, key).lowest_sell.price
                for key, value in revenue["net_income"].__dict__.items()
                if key != "money"
            }
        )
        revenue["trade_bonus"] = bonus
        return revenue

    # PHASE OUT
    async def _make_alliance(self) -> None:
        pass

    async def _make_user(self) -> None:
        pass

    async def _make_partial_cities(self) -> None:
        pass
