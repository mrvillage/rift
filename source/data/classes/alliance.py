from .base import Base
from ..query import get_alliance
from ...funcs import utils
import json
from ... import cache


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

    def __repr__(self):
        return f"{self.id}-{self.name}"

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
                    self.id and i.alliance_position in ("Member", "Officer", "Heir", "Leader") and i.v_mode]
        else:
            return [i for i in cache.nations.values() if i.alliance_id ==
                    self.id and i.alliance_position in ("Member", "Officer", "Heir", "Leader") and not i.v_mode]

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
