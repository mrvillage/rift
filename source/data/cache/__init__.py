from __future__ import print_function
from .alliance import *
# from . import cache
from .city import *
from .database import *
from .nation import *
from ...funcs import bot
from functools import partial
import asyncio
from .. import query

import time
from sys import getsizeof, stderr
from itertools import chain
from collections import deque

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

async def create_cache(*, alliance_data=None, city_data=None, nation_data=None, document_data=None, server_data=None):
    nation_data = await query.get_nations()
    alliance_data = await query.get_alliances()
    city_data = await query.get_cities()
    document_data = await query.get_documents()
    server_data = await query.get_servers()
    await create_cache_documents(document_data=document_data)
    await create_cache_servers(server_data=server_data)
    await create_cache_cities(city_data=city_data)
    await create_cache_nations(nation_data=nation_data)
    await create_cache_alliances(alliance_data=alliance_data)
    s = list(cache.nations.values())+list(cache.alliances.values())+list(cache.cities.values())+list(cache.documents.values())+list(cache.servers.values())
    s = [list(i.data) for i in s]
    await link_cache_cities()
    await link_cache_nations()
    print("Cache Created")