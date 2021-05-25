from .base import Base
from ..query import get_alliance
from ... import cache
from ...funcs.parse import parse_alliance_bank
from ...ref import bot
from .resources import Resources
from ...find import search_alliance


class Alliance(Base):
    def __init__(self, *, alliance_id=None, alliance_name=None, data=None):
        if data is None:
            self.data = get_alliance(
                alliance_id=alliance_id, alliance_name=alliance_name)
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
                alliance_id=alliance_id, alliance_name=alliance_name)
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

    def list_members(self, vm=None):
        if vm is None:
            return [i for i in cache.nations.values() if i.alliance_id ==
                    self.id and i.alliance_position in ("Member", "Officer", "Heir", "Leader")]
        elif vm:
            return [i for i in cache.nations.values() if i.alliance_id ==
                    self.id and
                    i.alliance_position in ("Member", "Officer", "Heir", "Leader") and
                    i.v_mode]
        else:
            return [i for i in cache.nations.values() if i.alliance_id ==
                    self.id and
                    i.alliance_position in ("Member", "Officer", "Heir", "Leader") and
                    not i.v_mode]

    def list_applicants(self):
        return [i for i in cache.nations.values() if i.alliance_id ==
                self.id and i.alliance_position == "Applicant"]

    def list_officers(self):
        return [i for i in cache.nations.values() if i.alliance_id ==
                self.id and i.alliance_position == "Officer"]

    def list_heirs(self):
        return [i for i in cache.nations.values() if i.alliance_id ==
                self.id and i.alliance_position == "Heir"]

    def list_leaders(self):
        return [i for i in cache.nations.values() if i.alliance_id ==
                self.id and i.alliance_position == "Leader"]

    def get_militarization(self, vm=None):
        members = self.list_members(vm=vm)
        cities = sum(i.cities for i in members)
        militarization = {
            "soldiers": sum(i.soldiers for i in members)/(cities*15000),
            "tanks": sum(i.tanks for i in members)/(cities*1250),
            "aircraft": sum(i.aircraft for i in members)/(cities*75),
            "ships": sum(i.ships for i in members)/(cities*15),
        }
        militarization["total"] = sum(militarization.values())/4
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
