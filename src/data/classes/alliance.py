from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union

import cachetools
import discord
import pnwkit
from pnwkit.async_ import AsyncKit

from ...cache import cache
from ...errors import AllianceNotFoundError, NoCredentialsError
from ...find import search_alliance
from ...flags import RolePermissions
from ...ref import RiftContext
from .base import Makeable
from .city import City
from .resources import Resources

__all__ = ("Alliance",)

if TYPE_CHECKING:
    from pnwkit.data import Alliance as PnWKitAlliance

    from _typings import AllianceData, Field, RevenueDict

    from .nation import Nation
    from .trade import TradePrices
    from .treaty import Treaty


class Alliance(Makeable):
    __slots__ = (
        "id",
        "found_date",
        "name",
        "acronym",
        "color",
        "rank",
        "flag_url",
        "forum_url",
        "ircchan",
    )

    def __init__(self, data: AllianceData) -> None:
        self.id: int = data["id"]
        self.found_date: str = data["found_date"]
        self.name: str = data["name"]
        self.acronym: str = data["acronym"]
        self.color: str = data["color"].capitalize()
        self.rank: int = data["rank"]
        self.flag_url: Optional[str] = data["flag_url"]
        self.forum_url: Optional[str] = data["forum_url"]
        self.ircchan: Optional[str] = data["ircchan"]

    @classmethod
    async def convert(
        cls, ctx: RiftContext, search: Any, advanced: bool = True
    ) -> Alliance:
        return await search_alliance(ctx, search, advanced)

    @classmethod
    async def fetch(cls, alliance_id: int) -> Alliance:
        alliance = cache.get_alliance(alliance_id)
        if alliance:
            return alliance
        raise AllianceNotFoundError(alliance_id)

    def update(self, data: AllianceData, /) -> None:
        self.id: int = data["id"]
        self.found_date: str = data["found_date"]
        self.name: str = data["name"]
        self.acronym: str = data["acronym"]
        self.color: str = data["color"].capitalize()
        self.rank: int = data["rank"]
        self.flag_url: Optional[str] = data["flag_url"]
        self.forum_url: Optional[str] = data["forum_url"]
        self.ircchan: Optional[str] = data["ircchan"]

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

    def __int__(self) -> int:
        return self.id

    def __float__(self) -> float:
        return sum(i.score for i in self.members)

    def __len__(self) -> int:
        return len(self.members)

    def __bool__(self) -> bool:
        return True

    @property
    def members(self) -> List[Nation]:
        return [
            i
            for i in cache.nations
            if i.alliance_id == self.id and i.alliance_position != 1 and not i.v_mode
        ]

    @property
    def vm_members(self) -> List[Nation]:
        return [
            i
            for i in cache.nations
            if i.alliance_id == self.id and i.v_mode and i.alliance_position != 1
        ]

    @property
    def leaders(self) -> List[Nation]:
        return [i for i in self.members if i.alliance_position == 5]

    @property
    def heirs(self) -> List[Nation]:
        return [i for i in self.members if i.alliance_position == 4]

    @property
    def officers(self) -> List[Nation]:
        return [i for i in self.members if i.alliance_position == 3]

    @property
    def applicants(self) -> List[Nation]:
        return [
            i
            for i in cache.nations
            if i.alliance_id == self.id and i.alliance_position == 1
        ]

    @property
    def score(self) -> float:
        return sum(i.score for i in self.members)

    @property
    @cachetools.cached(cache=cachetools.TTLCache(1024, 30))  # type: ignore
    def member_count(self) -> int:
        return len(self.members)

    @property
    def treaties(self) -> List[Treaty]:
        return [
            i
            for i in cache.treaties
            if (i.from_ and i.from_.id) == self.id or (i.to_ and i.to_.id) == self.id
        ]

    @property
    def soldiers(self) -> int:
        return sum(i.soldiers for i in self.members)

    @property
    def tanks(self) -> int:
        return sum(i.tanks for i in self.members)

    @property
    def aircraft(self) -> int:
        return sum(i.aircraft for i in self.members)

    @property
    def ships(self) -> int:
        return sum(i.ships for i in self.members)

    @property
    def missiles(self) -> int:
        return sum(i.missiles for i in self.members)

    @property
    def nukes(self) -> int:
        return sum(i.nukes for i in self.members)

    @property
    def cities(self) -> int:
        return sum(i.cities for i in self.members)

    @property
    def militarization(self) -> Dict[str, float]:
        cities = self.cities
        if not cities:
            return {"soldiers": 0, "tanks": 0, "aircraft": 0, "ships": 0, "total": 0}
        militarization = {
            "soldiers": self.soldiers / (cities * 15000),
            "tanks": self.tanks / (cities * 1250),
            "aircraft": self.aircraft / (cities * 75),
            "ships": self.ships / (cities * 15),
        }
        militarization["total"] = sum(militarization.values()) / 4
        return militarization

    @property
    def average_infrastructure(self) -> float:
        ids = {i.id for i in self.members}
        return (
            sum(i.infrastructure for i in cache.cities if i.nation_id in ids)
            / self.cities
            if self.cities
            else 0
        )

    @property
    def partial_cities(self) -> Set[City]:
        ids = {i.id for i in self.members}
        return {i for i in cache.cities if i.nation_id in ids}

    def get_info_embed(self, ctx: RiftContext, short: bool = False) -> discord.Embed:
        # sourcery no-metrics
        from ...funcs import get_embed_author_guild, get_embed_author_member

        member_count = self.member_count
        score = self.score
        leaders = self.leaders
        heirs = self.heirs
        officers = self.officers
        fields: List[Field] = [
            {"name": "Alliance ID", "value": self.id},
            {"name": "Alliance Name", "value": self.name},
            {
                "name": "Alliance Acronym",
                "value": self.acronym if self.acronym != "" else "None",
            },
            {"name": "Color", "value": self.color},
            {"name": "Rank", "value": f"#{self.rank}"},
            {
                "name": "Members",
                "value": f"[{member_count:,}](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(self.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true)",
            },
            {"name": "Score", "value": f"{score:,.2f}"},
            {
                "name": "Average Score",
                "value": f"{score/member_count if member_count != 0 else 0:,.2f}",
            },
            {
                "name": "Applicants",
                "value": f"{len(self.applicants):,}",
            },
            {
                "name": "Leaders",
                "value": "\n".join(
                    f"[{repr(i)}](https://politicsandwar.com/nation/id={i.id})"
                    for i in leaders
                )
                if leaders and not short
                else ", ".join(str(i.id) for i in leaders)
                if leaders and short
                else "None",
            },
            {
                "name": "Heirs",
                "value": "\n".join(
                    f"[{repr(i)}](https://politicsandwar.com/nation/id={i.id})"
                    for i in heirs
                )
                if heirs and not short
                else ", ".join(str(i.id) for i in heirs)
                if heirs and short
                else "None",
            },
            {
                "name": "Officers",
                "value": "\n".join(
                    f"[{repr(i)}](https://politicsandwar.com/nation/id={i.id})"
                    for i in officers
                )
                if officers and not short
                else ", ".join(str(i.id) for i in officers)
                if officers and short
                else "None",
            },
            {
                "name": "Forum Link",
                "value": f'[Click Here]({self.forum_url} "{self.forum_url}")'
                if self.forum_url is not None
                else "None",
            },
            {
                "name": "Discord Link",
                "value": f'[Click Here]({self.ircchan} "{self.ircchan}")'
                if self.ircchan is not None
                else "None",
            },
            {
                "name": "Vacation Mode",
                "value": f"{len(self.vm_members):,}",
            },
            {
                "name": "Average Cities",
                "value": f"{self.cities/member_count if member_count else 0:,.2f}",
            },
            {
                "name": "Average Infrastructure",
                "value": f"{self.average_infrastructure:,.2f}",
            },
            {
                "name": "Treasures",
                "value": len(
                    [
                        i
                        for i in cache.treasures
                        if (i.nation and i.nation.alliance) is self
                    ]
                ),
            },
        ]
        embed = (
            get_embed_author_guild(
                ctx,  # this is here if it ever gets passed as a Guild for some reason
                f"[Alliance Page](https://politicsandwar.com/alliance/id={self.id})\n[War Activity](https://politicsandwar.com/alliance/id={self.id}&display=war)",
                timestamp=datetime.fromisoformat(self.found_date),
                footer="Alliance created",
                fields=fields,
                color=discord.Color.blue(),
            ).set_thumbnail(url=self.flag_url)
            if isinstance(ctx, discord.Guild)
            else get_embed_author_member(
                ctx.author,
                f"[Alliance Page](https://politicsandwar.com/alliance/id={self.id})\n[War Activity](https://politicsandwar.com/alliance/id={self.id}&display=war)",
                timestamp=datetime.fromisoformat(self.found_date),
                footer="Alliance created",
                fields=fields,
                color=discord.Color.blue(),
            ).set_thumbnail(url=self.flag_url)
        )
        if any(len(fields[i]["value"] + fields[i]["name"]) > 1024 for i in {9, 10, 11}):
            return self.get_info_embed(ctx, short=True)
        return embed

    async def calculate_revenue(
        self,
        prices: Optional[TradePrices] = None,
        data: Optional[PnWKitAlliance] = None,
        fetch_spies: bool = False,
    ) -> RevenueDict:
        prices = prices or cache.prices
        if data is None:
            raw_data = await pnwkit.async_alliance_query(
                {"id": self.id, "first": 1},
                {
                    "nations": (
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
                    ),
                },
            )
            data = raw_data[0]
        if TYPE_CHECKING:
            assert isinstance(data, tuple)
        prices = cache.prices
        nations = {int(i.id): i for i in data["nations"]}
        revenues = [
            await i.calculate_revenue(
                prices,
                nations.get(i.id),
                fetch_spies,
            )
            for i in self.members
            if nations.get(i.id) is not None
        ]
        return {
            "gross_income": sum(
                (i["gross_income"] for i in revenues[1:]), revenues[0]["gross_income"]
            ),
            "net_income": sum(
                (i["net_income"] for i in revenues[1:]), revenues[0]["net_income"]
            ),
            "gross_total": sum(
                (i["gross_total"] for i in revenues[1:]), revenues[0]["gross_total"]
            ),
            "net_total": sum(
                (i["net_total"] for i in revenues[1:]), revenues[0]["net_total"]
            ),
            "upkeep": sum((i["upkeep"] for i in revenues[1:]), revenues[0]["upkeep"]),
            "upkeep_total": sum(
                (i["upkeep_total"] for i in revenues[1:]), revenues[0]["upkeep_total"]
            ),
        }

    async def fetch_bank(self) -> Resources:
        from ...funcs import credentials

        credentials = credentials.find_highest_alliance_credentials(
            self, "view_alliance_bank"
        )
        if credentials is None or credentials.api_key is None:
            raise NoCredentialsError(self)

        kit = AsyncKit(credentials.api_key)
        data = await kit.alliance_query(
            {"id": self.id, "first": 1},
            "money",
            "coal",
            "oil",
            "uranium",
            "iron",
            "bauxite",
            "lead",
            "gasoline",
            "munitions",
            "steel",
            "aluminum",
            "food",
        )
        bank = data[0]
        if bank.money is None:
            raise NoCredentialsError(self)
        return Resources.from_dict(bank)  # type: ignore

    def permissions_for(
        self, user: Union[discord.User, discord.Member]
    ) -> RolePermissions:
        return self.permissions_for_id(self.id, user)

    @staticmethod
    def permissions_for_id(
        alliance_id: int, user: Union[discord.User, discord.Member]
    ) -> RolePermissions:
        link = cache.get_user(user.id)
        nation = cache.get_nation(link.nation_id) if link is not None else None
        alliance_position = (
            nation.alliance_position
            if nation is not None and nation.alliance_id == alliance_id
            else 0
        )
        roles = (
            i
            for i in cache.roles
            if i.alliance_id == alliance_id
            and (user.id in i.member_ids or alliance_position in i.alliance_positions)
        )
        permissions = sum(
            (i.permissions for i in roles),
            RolePermissions(),
        )
        if alliance_position >= 4:
            permissions.leadership = True
        permissions.max_rank = max(i.rank for i in roles) if roles else 0
        return permissions
