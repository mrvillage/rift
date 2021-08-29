from __future__ import annotations

from datetime import datetime
from typing import Dict, Union

from discord import Embed, Guild
from discord.ext.commands.context import Context
from src.data.query.alliance import query_applicants, query_members

from ...errors import AllianceNotFoundError
from ...find import search_alliance
from ...ref import bot
from ..query import query_alliance
from .base import Makeable
from .resources import Resources


class Alliance(Makeable):
    __slots__ = (
        "data",
        "id",
        "founddate",
        "name",
        "acronym",
        "color",
        "rank",
        "score",
        "avgscore",
        "flagurl",
        "forumurl",
        "ircchan",
        "discord",
        "members",
        "vm_members",
        "leaders",
        "heirs",
        "officers",
        "applicants",
        "calculated_score",
        "member_count",
        "treaties",
    )

    def __init__(self, *, alliance_id=None, alliance_name=None, data=None):
        if data is None:
            self.data = query_alliance(
                alliance_id=alliance_id, alliance_name=alliance_name
            )
        else:
            self.data = data
        self.id = self.data[0]
        self.founddate = self.data[1]
        self.name = self.data[2]
        self.acronym = self.data[3]
        self.color = self.data[4].capitalize()
        self.rank = self.data[5]
        self.score = self.data[7]
        self.avgscore = self.data[11]
        self.flagurl = self.data[12] if self.data[12] is not None else None
        self.forumurl = self.data[13] if self.data[13] is not None else None
        self.ircchan = self.data[14] if self.data[14] is not None else None
        self.discord = self.ircchan

    def __repr__(self):
        return f"{self.id} - {self.name}"

    def _update(self, *, alliance_id=None, alliance_name=None, data=None):
        if data is None:
            self.data = query_alliance(
                alliance_id=alliance_id, alliance_name=alliance_name
            )
        else:
            self.data = data
        self.id = self.data[0]
        self.founddate = self.data[1]
        self.name = self.data[2]
        self.acronym = self.data[3]
        self.color = self.data[4].capitalize()
        self.rank = self.data[5]
        self.score = self.data[7]
        self.avgscore = self.data[11]
        self.flagurl = self.data[12] if self.data[12] is not None else None
        self.forumurl = self.data[13] if self.data[13] is not None else None
        self.ircchan = self.data[14] if self.data[14] is not None else None
        return self

    def get_militarization(self, vm=None):
        cities = sum(i.cities for i in self.members if not i.v_mode)
        militarization = {
            "soldiers": sum(i.soldiers for i in self.members if not i.v_mode)
            / (cities * 15000),
            "tanks": sum(i.tanks for i in self.members if not i.v_mode)
            / (cities * 1250),
            "aircraft": sum(i.aircraft for i in self.members if not i.v_mode)
            / (cities * 75),
            "ships": sum(i.ships for i in self.members if not i.v_mode) / (cities * 15),
        }
        militarization["total"] = sum(militarization.values()) / 4
        return militarization

    def get_soldiers(self, vm=None):
        return sum(i.soldiers for i in self.members if not i.v_mode)

    def get_tanks(self, vm=None):
        return sum(i.tanks for i in self.members if not i.v_mode)

    def get_aircraft(self, vm=None):
        return sum(i.aircraft for i in self.members if not i.v_mode)

    def get_ships(self, vm=None):
        return sum(i.ships for i in self.members if not i.v_mode)

    def get_missiles(self, vm=None):
        return sum(i.missiles for i in self.members if not i.v_mode)

    def get_nukes(self, vm=None):
        return sum(i.nukes for i in self.members if not i.v_mode)

    def get_cities(self, vm=None):
        return sum(i.cities for i in self.members if not i.v_mode)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def list_members(self, vm):
        try:
            return self.members
        except AttributeError:
            return []

    def __float__(self):
        return sum(i[0] for i in self.list_members(vm=False))

    def __len__(self):
        return len([i[0] for i in self.list_members(vm=False)])

    async def get_resources(self):
        from ...funcs import parse_alliance_bank

        async with bot.pnw_session.request(
            "GET", f"https://politicsandwar.com/alliance/id={self.id}&display=bank"
        ) as response:
            content = await response.text()
        await bot.parse_token(content)
        return await Resources.from_dict(await parse_alliance_bank(content))

    @classmethod
    async def convert(cls, ctx, search):
        return await search_alliance(ctx, search)

    @classmethod
    async def fetch(cls, alliance_id: Union[int, str] = None) -> Alliance:
        try:
            return cls(data=await query_alliance(alliance_id=alliance_id))
        except IndexError:
            raise AllianceNotFoundError(alliance_id)

    async def _make_members(self) -> None:
        from .nation import Nation

        members = await query_members(alliance_id=self.id)
        members = [tuple(i) for i in members]
        self.members = [Nation(data=i) for i in members]

    async def _make_vm_members(self) -> None:
        self.vm_members = [i for i in self.members if i.v_mode]

    async def _make_leaders(self) -> None:
        self.leaders = [i for i in self.members if i.alliance_position == "Leader"]

    async def _make_heirs(self) -> None:
        self.heirs = [i for i in self.members if i.alliance_position == "Heir"]

    async def _make_officers(self) -> None:
        self.officers = [i for i in self.members if i.alliance_position == "Officer"]

    async def _make_applicants(self) -> None:
        from .nation import Nation

        applicants = await query_applicants(alliance_id=self.id)
        applicants = [tuple(i) for i in applicants]
        self.applicants = [Nation(data=i) for i in applicants]

    async def _make_calculated_score(self) -> None:
        self.calculated_score = sum(i.score for i in self.members if not i.v_mode)

    async def _make_member_count(self) -> None:
        self.member_count = len([i for i in self.members if not i.v_mode])

    async def _make_treaties(self) -> None:
        from .treaty import Treaties

        self.treaties = await Treaties.fetch(self)

    async def get_info_embed(self, ctx: Context) -> Embed:
        from ...funcs import get_embed_author_guild, get_embed_author_member

        await self.make_attrs(
            "members",
            "vm_members",
            "leaders",
            "heirs",
            "officers",
            "applicants",
            "calculated_score",
            "member_count",
        )
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
            {"name": "Score", "value": f"{self.calculated_score:,.2f}"},
            {
                "name": "Average Score",
                "value": f"{self.calculated_score/self.member_count if self.member_count != 0 else 0:,.2f}",
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
                if len(self.leaders) != 0
                else "None",
            },
            {
                "name": "Heirs",
                "value": "\n".join(
                    f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                    for i in self.heirs
                )
                if len(self.heirs) != 0
                else "None",
            },
            {
                "name": "Officers",
                "value": "\n".join(
                    f'[{repr(i)}](https://politicsandwar.com/nation/id={i.id} "https://politicsandwar.com/nation/id={i.id}")'
                    for i in self.officers
                )
                if len(self.officers) != 0
                else "None",
            },
            {
                "name": "Forum Link",
                "value": f'[Click Here]({self.forumurl} "{self.forumurl}")'
                if self.forumurl is not None
                else "None",
            },
            {
                "name": "Discord Link",
                "value": f'[Click Here]({self.discord} "{self.discord}")'
                if self.discord is not None
                else "None",
            },
            {
                "name": "Vacation Mode",
                "value": f"{len(self.vm_members):,}",
            },
        ]
        return (
            get_embed_author_guild(
                ctx,  # this is here if it ever gets passed as a Guild for some reason
                f'[Alliance Page](https://politicsandwar.com/alliance/id={self.id} "https://politicsandwar.com/alliance/id={self.id}")\n[War Activity](https://politicsandwar.com/alliance/id={self.id}&display=war "https://politicsandwar.com/alliance/id={self.id}&display=war")',
                timestamp=datetime.fromisoformat(self.founddate),
                footer="Alliance created",
                fields=fields,
            ).set_thumbnail(url=self.flagurl)
            if isinstance(ctx, Guild)
            else get_embed_author_member(
                ctx.author,
                f'[Alliance Page](https://politicsandwar.com/alliance/id={self.id} "https://politicsandwar.com/alliance/id={self.id}")\n[War Activity](https://politicsandwar.com/alliance/id={self.id}&display=war "https://politicsandwar.com/alliance/id={self.id}&display=war")',
                timestamp=datetime.fromisoformat(self.founddate),
                footer="Alliance created",
                fields=fields,
            ).set_thumbnail(url=self.flagurl)
        )

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
