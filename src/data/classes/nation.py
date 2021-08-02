from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Sequence, Union
from urllib.parse import quote

import aiohttp
from aiohttp import request
from bs4 import BeautifulSoup
from discord import Embed, Guild, NotFound, User
from discord.ext.commands import Context
from discord.utils import valid_icon_size

from ...data.get import get_link_nation
from ...errors import NationNotFoundError, SentError
from ...find import search_nation
from ...funcs import utils
from ..query import get_nation
from ..query.city import get_nation_cities
from .base import Embedable, Fetchable, Initable, Makeable

if TYPE_CHECKING:
    from .alliance import Alliance


class Nation(Embedable, Fetchable, Initable, Makeable):
    def __init__(self, *, nation_id=None, nation_name=None, data=None):
        if data is None:
            self.data = get_nation(nation_id=nation_id, nation_name=nation_name)
        else:
            self.data = data
        self.id = self.data[0]
        self.name = self.data[1]
        self.leader = self.data[2]
        self.continent = utils.get_continent(self.data[3])
        self.war_policy = utils.get_war_policy(self.data[4])
        self.domestic_policy = utils.get_domestic_policy(self.data[5])
        self.color = utils.get_color(self.data[6])
        self.alliance_id = self.data[7]
        self.alliance = self.data[8] if self.data[8] != "None" else None
        self.alliance_position = utils.get_alliance_position(self.data[9])
        self.cities = self.data[10]
        self.offensive_wars = self.data[11]
        self.defensive_wars = self.data[12]
        self.score = self.data[13]
        self.v_mode = self.data[14]
        self.v_mode_turns = self.data[15]
        self.beige_turns = self.data[16]
        self.last_active = self.data[17]
        self.founded = self.data[18]
        self.soldiers = self.data[19]
        self.tanks = self.data[20]
        self.aircraft = self.data[21]
        self.ships = self.data[22]
        self.missiles = self.data[23]
        self.nukes = self.data[24]

    def __repr__(self):
        return f"{self.id} - {self.name}"

    def _update(self, *, nation_id=None, nation_name=None, data=None):
        if data is None:
            self.data = get_nation(nation_id=nation_id, nation_name=nation_name)
        else:
            self.data = data
        self.id = self.data[0]
        self.name = self.data[1]
        self.leader = self.data[2]
        self.continent = utils.get_continent(self.data[3])
        self.war_policy = utils.get_war_policy(self.data[4])
        self.domestic_policy = utils.get_domestic_policy(self.data[5])
        self.color = utils.get_color(self.data[6])
        self.alliance_id = self.data[7]
        self.alliance = self.data[8] if self.data[8] != "None" else None
        self.alliance_position = utils.get_alliance_position(self.data[9])
        self.cities = self.data[10]
        self.offensive_wars = self.data[11]
        self.defensive_wars = self.data[12]
        self.score = self.data[13]
        self.v_mode = self.data[14]
        self.v_mode_turns = self.data[15]
        self.beige_turns = self.data[16]
        self.last_active = self.data[17]
        self.founded = self.data[18]
        self.soldiers = self.data[19]
        self.tanks = self.data[20]
        self.aircraft = self.data[21]
        self.ships = self.data[22]
        self.missiles = self.data[23]
        self.nukes = self.data[24]
        return self

    async def send_message(self, *, subject=None, content=None):
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
            if "successfully" in (await response.text()).lower():
                return True
            else:
                return SentError

    def get_militarization(self):
        militarization = {
            "soldiers": self.soldiers / (self.cities * 15000),
            "tanks": self.tanks / (self.cities * 1250),
            "aircraft": self.aircraft / (self.cities * 75),
            "ships": self.ships / (self.cities * 15),
        }
        militarization["total"] = sum(militarization.values()) / 4
        return militarization

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __float__(self):
        return self.score

    def __len__(self):
        return self.cities

    def get_average_infrastructure(self):
        return sum(i.infrastructure for i in self.partial_cities) / self.cities

    avg_infra = get_average_infrastructure

    async def get_discord_page_username(self):
        async with request(
            "GET", f"https://politicsandwar.com/nation/id={self.id}"
        ) as response:
            return [
                i.contents[1].text
                for i in BeautifulSoup(await response.text(), "html.parser").find_all(
                    "tr", class_="notranslate"
                )
                if any("Discord Username:" in str(j) for j in i.contents)
            ][0]

    @classmethod
    async def convert(cls, ctx, search):
        return await search_nation(ctx, search)

    async def get_revenue_modifiers(self):
        pass

    async def get_revenue(self):
        return (
            sum(city.get_revenue() for city in self.list_cities())
            + self.get_revenue_modifiers()
        )

    @classmethod
    async def fetch(cls, nation_id: Union[int, str] = None) -> Nation:
        try:
            return cls(data=await get_nation(nation_id=nation_id))
        except IndexError:
            raise NationNotFoundError

    async def _make_alliance(self) -> None:
        from .alliance import Alliance

        if self.alliance_id != 0:
            self.alliance = await Alliance.fetch(self.alliance_id)

    async def _make_user(self) -> User:
        from ...ref import bot

        try:
            self.user = await bot.fetch_user((await get_link_nation(self.id))[0])
        except (IndexError, NotFound):
            self.user = None

    async def _make_partial_cities(self):
        from .city import City

        partial_cities = await get_nation_cities(self.id)
        partial_cities = [tuple(i) for i in partial_cities]
        self.partial_cities = [City(data=i) for i in partial_cities]

    async def get_info_embed(self, ctx: Context) -> Embed:
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
            get_embed_author_guild(
                ctx.guild,
                f'[Nation Page](https://politicsandwar.com/nation/id={self.id} "https://politicsandwar.com/nation/id={self.id}")',
                timestamp=datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
            )
            if self.user is None
            else get_embed_author_member(
                self.user,
                f'[Nation Page](https://politicsandwar.com/nation/id={self.id} "https://politicsandwar.com/nation/id={self.id}")',
                timestamp=datetime.fromisoformat(self.founded),
                footer="Nation created",
                fields=fields,
            )
        )

    async def scrape_city_manager(self) -> Sequence[Dict[str, Any]]:
        from ...funcs.utils import convert_link

        async with aiohttp.request(
            "GET", f"https://politicsandwar.com/city/manager/n={quote(self.name)}"
        ) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
        table = soup.find_all(class_="nationtable")[1]
        rows = table.find_all("tr")
        ids = [
            int(await convert_link(i.contents[0].attrs["href"]))
            for i in rows[0].contents[2:]
        ]
        del rows[:2]
        items = [(row.contents[0].contents[0].contents[0].lower().replace(" ", "_"), row) for row in rows]
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
