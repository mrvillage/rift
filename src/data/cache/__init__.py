from .. import query
from .alliance import *
from .city import *
from .database import *
from .nation import *


async def create_cache(
    *,
    alliance_data=None,
    city_data=None,
    nation_data=None,
    document_data=None,
    server_data=None
):
    nation_data = await query.query_nations()
    alliance_data = await query.query_alliances()
    city_data = await query.query_cities()
    document_data = await query.query_documents()
    server_data = await query.query_servers()
    await create_cache_documents(document_data=document_data)
    await create_cache_servers(server_data=server_data)
    await create_cache_cities(city_data=city_data)
    await create_cache_nations(nation_data=nation_data)
    await create_cache_alliances(alliance_data=alliance_data)
    s = (
        list(cache.nations.values())
        + list(cache.alliances.values())
        + list(cache.cities.values())
        + list(cache.documents.values())
        + list(cache.servers.values())
    )
    s = [list(i.data) for i in s]
    await link_cache_cities()
    await link_cache_nations()
    print("Cache Created")
