from .base import Base
from ..query import get_nation
from ...funcs import utils
import aiohttp
from ...funcs.core import bot
from ...errors import SentError
from ... import cache


class Nation(Base):
    def __init__(self, *, nation_id=None, nation_name=None, data=None):
        if data is None:
            self.data = get_nation(nation_id=nation_id,
                                   nation_name=nation_name)
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
            self.data = get_nation(nation_id=nation_id,
                                   nation_name=nation_name)
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

    async def _link(self):
        try:
            self.alliance = cache.alliances[self.alliance_id] if self.alliance is not None else None
        except KeyError:
            self.alliance = None

    def list_cities(self):
        return [i for i in cache.cities.values() if i.nation_id == self.id]

    async def send_message(self, *, subject=None, content=None):
        message_data = {
            "newconversation": "true",
            "receiver": self.leader,
            "subject": subject,
            "body": content,
            "sndmsg": "Send Message"
        }
        async with bot.pnw_session.post("https://politicsandwar.com/inbox/message", data=message_data, timeout=30.0) as response:
            if "successfully" in (await response.text()).lower():
                return True
            else:
                return SentError

    def get_militarization(self):
        militarization = {
            "soldiers": self.soldiers/(self.cities*15000),
            "tanks": self.tanks/(self.cities*1250),
            "aircraft": self.aircraft/(self.cities*75),
            "ships": self.ships/(self.cities*15),
        }
        militarization['total'] = sum(militarization.values())/4
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
        return sum(i.infrastructure for i in cache.cities.values() if i.nation_id == self.id)/self.cities
    
    avg_infra = get_average_infrastructure