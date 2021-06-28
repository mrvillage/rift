from ..classes.nation import Nation
from ... import cache
import asyncio


async def create_cache_nations(*, nation_data):
    counter = 0
    for data in nation_data:
        counter += 1
        cache.nations[data[0]] = Nation(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def refresh_cache_nations(*, nation_data):
    counter = 0
    for data in nation_data:
        counter += 1
        try:
            nation = cache.nations[data[0]]
            nation._update(data=data)
        except KeyError:
            cache.nations[data[0]] = Nation(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def link_cache_nations():
    counter = 0
    for nation in cache.nations.values():
        counter += 1
        await nation._link()
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0
