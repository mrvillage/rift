from __future__ import annotations

from datetime import datetime
from src.data.query.alliance import get_applicants, get_members
from typing import Union

from discord import Embed, Guild
from discord.ext.commands.context import Context

from ...errors import AllianceNotFoundError
from ...find import search_alliance
from ...funcs.parse import parse_alliance_bank
from ...ref import bot
from ..query import get_alliance
from .base import Base
from .resources import Resources


class Alliance(Base):
    def __init__(self, *, alliance_id=None, alliance_name=None, data=None):
        if data is None:
            self.data = get_alliance(
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
            self.data = get_alliance(
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
        cities = sum(i.cities for i in self.members)
        militarization = {
            "soldiers": sum(i.soldiers for i in self.members) / (cities * 15000),
            "tanks": sum(i.tanks for i in self.members) / (cities * 1250),
            "aircraft": sum(i.aircraft for i in self.members) / (cities * 75),
            "ships": sum(i.ships for i in self.members) / (cities * 15),
        }
        militarization["total"] = sum(militarization.values()) / 4
        return militarization

    def get_soldiers(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.soldiers for i in members)

    def get_tanks(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.tanks for i in members)

    def get_aircraft(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.aircraft for i in members)

    def get_ships(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.ships for i in members)

    def get_missiles(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.missiles for i in members)

    def get_nukes(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.nukes for i in members)

    def get_cities(self, vm=None):
        members = self.list_members(vm=vm)
        return sum(i.cities for i in members)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __float__(self):
        return sum(i[0] for i in self.list_members(vm=False))

    def __len__(self):
        return len([i[0] for i in self.list_members(vm=False)])

    async def get_resources(self):
        async with bot.pnw_session.request(
            "GET", "https://politicsandwar.com/alliance/id=7719&display=bank"
        ) as response:
            content = await response.text()
        await bot.parse_token(content)
        return await Resources.from_dict(await parse_alliance_bank(content))

    @classmethod
    async def convert(cls, ctx, search):
        return await search_alliance(ctx, search)

    async def get_revenue_modifiers(self):
        pass

    async def get_revenue(self):
        return (
            sum(nation.get_revenue() for nation in self.list_members(vm=False))
            + self.get_revenue_modifiers()
        )

    @classmethod
    async def fetch(cls: Alliance, alliance_id: Union[int, str] = None) -> Alliance:
        try:
            return cls(data=await get_alliance(alliance_id=alliance_id))
        except IndexError:
            raise AllianceNotFoundError

    async def _make_members(self: Alliance) -> None:
        from .nation import Nation

        members = await get_members(alliance_id=self.id)
        members = [tuple(i) for i in members]
        self.members = [Nation(data=i) for i in members]

    async def _make_vm_members(self: Alliance) -> None:
        self.vm_members = [i for i in self.members if i.v_mode]

    async def _make_leaders(self: Alliance) -> None:
        self.leaders = [i for i in self.members if i.alliance_position == "Leader"]

    async def _make_heirs(self: Alliance) -> None:
        self.heirs = [i for i in self.members if i.alliance_position == "Heir"]

    async def _make_officers(self: Alliance) -> None:
        self.officers = [i for i in self.members if i.alliance_position == "Officer"]

    async def _make_applicants(self: Alliance) -> None:
        from .nation import Nation

        applicants = await get_applicants(alliance_id=self.id)
        applicants = [tuple(i) for i in applicants]
        self.applicants = [Nation(data=i) for i in applicants]

    async def _make_calculated_score(self: Alliance) -> None:
        self.calculated_score = sum(i.score for i in self.members)

    async def get_info_embed(self: Alliance, ctx: Context) -> Embed:
        from ...funcs import get_embed_author_guild, get_embed_author_member

        await self.make_attrs(
            "members",
            "vm_members",
            "leaders",
            "heirs",
            "officers",
            "applicants",
            "calculated_score",
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
                "value": f"[{len(self.members):,}](https://politicsandwar.com/index.php?id=15&keyword={'+'.join(self.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true \"https://politicsandwar.com/index.php?id=15&keyword={'+'.join(self.name.split(' '))}&cat=alliance&ob=score&od=DESC&maximum=50&minimum=0&search=Go&memberview=true\")",
            },
            {"name": "Score", "value": f"{self.calculated_score:,.2f}"},
            {
                "name": "Average Score",
                "value": f"{self.calculated_score/len(self.members) if len(self.members) != 0 else 0:,.2f}",
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
