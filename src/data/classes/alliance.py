from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Optional, Union

import discord
from discord.ext.commands.context import Context

from ...cache import cache
from ...errors import AllianceNotFoundError
from ...find import search_alliance
from ...ref import bot
from .base import Makeable
from .resources import Resources

__all__ = ("Alliance",)

if TYPE_CHECKING:
    from typings import AllianceData

    from .nation import Nation
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
    async def convert(cls, ctx, search) -> Alliance:
        return await search_alliance(ctx, search)

    @classmethod
    async def fetch(cls, alliance_id: int) -> Alliance:
        alliance = cache.get_alliance(alliance_id)
        if alliance:
            return alliance
        raise AllianceNotFoundError(alliance_id)

    def _update(self, data: AllianceData, /) -> None:
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

    def __str__(self) -> str:
        return self.name

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
        return [i for i in cache.nations if i.alliance_id == self.id]

    @property
    def vm_members(self) -> List[Nation]:
        return [i for i in cache.nations if i.alliance_id == self.id and i.v_mode]

    @property
    def leaders(self) -> List[Nation]:
        return [i for i in self.members if i.alliance_position == "Leader"]

    @property
    def heirs(self) -> List[Nation]:
        return [i for i in self.members if i.alliance_position == "Heir"]

    @property
    def officers(self) -> List[Nation]:
        return [i for i in self.members if i.alliance_position == "Officer"]

    @property
    def applicants(self) -> List[Nation]:
        return [
            i
            for i in cache.nations
            if i.alliance_id == self.id and i.alliance_position == "Applicant"
        ]

    @property
    def score(self) -> float:
        return sum(i.score for i in self.members)

    @property
    def member_count(self) -> int:
        return len(self.members)

    @property
    def treaties(self) -> List[Treaty]:
        return [i for i in cache.treaties if i.from_ == self.id or i.to_ == self.id]

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
        militarization = {
            "soldiers": self.soldiers / (self.cities * 15000),
            "tanks": self.tanks / (self.cities * 1250),
            "aircraft": self.aircraft / (self.cities * 75),
            "ships": self.ships / (self.cities * 15),
        }
        militarization["total"] = sum(militarization.values()) / 4
        return militarization

    async def get_resources(self) -> Resources:
        from ...funcs import parse_alliance_bank

        async with bot.pnw_session.request(
            "GET", f"https://politicsandwar.com/alliance/id={self.id}&display=bank"
        ) as response:
            content = await response.text()
        await bot.parse_token(content)
        return await Resources.from_dict(await parse_alliance_bank(content))

    async def get_info_embed(self, ctx: Context, short: bool = False) -> discord.Embed:
        # sourcery no-metrics
        from ...funcs import get_embed_author_guild, get_embed_author_member

        fields = [
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
                "value": f"[{self.member_count:,}](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(self.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true \"https://politicsandwar.com/index.php?id=15&keyword={'+'.join(self.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true\")",
            },
            {"name": "Score", "value": f"{self.score:,.2f}"},
            {
                "name": "Average Score",
                "value": f"{self.score/self.member_count if self.member_count != 0 else 0:,.2f}",
            },
            {
                "name": "Applicants",
                "value": f"{len(self.applicants):,}",
            },
            {
                "name": "Leaders",
                "value": "\n".join(
                    f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                    for i in self.leaders
                )
                if self.leaders and not short
                else ", ".join(str(i.id) for i in self.leaders)
                if self.leaders and short
                else "None",
            },
            {
                "name": "Heirs",
                "value": "\n".join(
                    f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                    for i in self.heirs
                )
                if self.heirs and not short
                else ", ".join(str(i.id) for i in self.heirs)
                if self.heirs and short
                else "None",
            },
            {
                "name": "Officers",
                "value": "\n".join(
                    f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                    for i in self.officers
                )
                if self.officers and not short
                else ", ".join(str(i.id) for i in self.officers)
                if self.officers and short
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
        ]
        embed = (
            get_embed_author_guild(
                ctx,  # this is here if it ever gets passed as a Guild for some reason
                f'[Alliance Page](https://politicsandwar.com/alliance/id={self.id} "https://politicsandwar.com/alliance/id={self.id}")\n[War Activity](https://politicsandwar.com/alliance/id={self.id}&display=war "https://politicsandwar.com/alliance/id={self.id}&display=war")',
                timestamp=datetime.fromisoformat(self.found_date),
                footer="Alliance created",
                fields=fields,
                color=discord.Color.blue(),
            ).set_thumbnail(url=self.flag_url)
            if isinstance(ctx, discord.Guild)
            else get_embed_author_member(
                ctx.author,
                f'[Alliance Page](https://politicsandwar.com/alliance/id={self.id} "https://politicsandwar.com/alliance/id={self.id}")\n[War Activity](https://politicsandwar.com/alliance/id={self.id}&display=war "https://politicsandwar.com/alliance/id={self.id}&display=war")',
                timestamp=datetime.fromisoformat(self.found_date),
                footer="Alliance created",
                fields=fields,
                color=discord.Color.blue(),
            ).set_thumbnail(url=self.flag_url)
        )
        if any(len(fields[i]["value"] + fields[i]["name"]) > 1024 for i in {9, 10, 11}):
            return await self.get_info_embed(ctx, short=True)
        return embed

    async def calculate_revenue(
        self,
    ) -> Dict[str, Union[Resources, Dict[str, float], int, float]]:
        from ...funcs import get_trade_prices

        await self.make_attrs("members")
        prices = await get_trade_prices()
        revenues = [await i.calculate_revenue(prices) for i in self.members]
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
        }

    # PHASE OUT
    def get_militarization(self, vm=None):
        return self.militarization

    def get_soldiers(self, vm=None):
        return self.soldiers

    def get_tanks(self, vm=None):
        return self.tanks

    def get_aircraft(self, vm=None):
        return self.aircraft

    def get_ships(self, vm=None):
        return self.ships

    def get_missiles(self, vm=None):
        return self.missiles

    def get_nukes(self, vm=None):
        return self.nukes

    def get_cities(self, vm=None):
        return self.cities

    async def _make_members(self) -> None:
        pass

    async def _make_vm_members(self) -> None:
        pass

    async def _make_leaders(self) -> None:
        pass

    async def _make_heirs(self) -> None:
        pass

    async def _make_officers(self) -> None:
        pass

    async def _make_applicants(self) -> None:
        pass

    async def _make_calculated_score(self) -> None:
        pass

    async def _make_member_count(self) -> None:
        pass

    async def _make_treaties(self) -> None:
        pass
