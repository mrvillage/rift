from ..classes import City
from ... import cache
import asyncio


async def create_cache_cities(*, city_data):
    counter = 0
    for data in city_data:
        counter += 1
        cache.cities[data[0]] = City(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def refresh_cache_cities(*, city_data):
    counter = 0
    for data in city_data:
        counter += 1
        try:
            city = cache.cities[data[0]]
            city._update(data=data)
        except KeyError:
            cache.cities[data[0]] = City(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def link_cache_cities():
    counter = 0
    for city in cache.cities.values():
        counter += 1
        await city._link()
        pass
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0
