from .base import Base
from ..query import get_city
from ...funcs import utils
from ... import cache
from ..requests import get_city_build


class City(Base):
    def __init__(self, *, city_id=None, city_name=None, data=None):
        if data is None:
            self.data = get_city(city_id=city_id, city_name=city_name)
        else:
            self.data = data
        self.id = self.data[0]
        self.nation_id = self.data[1]
        self.name = self.data[2]
        self.capital = self.data[3]
        self.infrastructure = self.data[4]
        self.maxinfra = self.data[5]
        self.land = self.data[6]

    def __repr__(self):
        return f"{self.id}-{self.name}"

    def _update(self, *, city_id=None, city_name=None, data=None):
        if data is None:
            self.data = get_city(city_id=city_id, city_name=city_name)
        else:
            self.data = data
        self.id = self.data[0]
        self.name = self.data[2]
        self.capital = self.data[3]
        self.infrastructure = self.data[4]
        self.maxinfra = self.data[5]
        self.land = self.data[6]
        return self

    async def _link(self):
        try:
            self.nation = cache.nations[self.nation_id]
        except KeyError:
            self.nation = None

    async def get_build(self):
        return await get_city_build(city_id=self.id)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __float__(self):
        return self.infrastructure, self.land
