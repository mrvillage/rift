from ..classes import Alliance
from ... import cache
import asyncio


async def create_cache_alliances(*, alliance_data):
    counter = 0
    for data in alliance_data:
        counter += 1
        cache.alliances[data[0]] = Alliance(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def refresh_cache_alliances(*, alliance_data):
    counter = 0
    for data in alliance_data:
        counter += 1
        try:
            alliance = cache.alliances[data[0]]
            alliance._update(data=data)
        except KeyError:
            cache.alliances[data[0]] = Alliance(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0
