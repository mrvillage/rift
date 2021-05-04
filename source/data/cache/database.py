from ..classes import Document, Server
from ... import cache
import asyncio
from ...funcs import utils


async def create_cache_documents(*, document_data):
    counter = 0
    for data in document_data:
        counter += 1
        cache.documents[data[0]] = Document(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def refresh_cache_documents(*, document_data):
    counter = 0
    for data in document_data:
        counter += 1
        document = await utils.find(lambda d: d.id == data[0], cache.documents.values())
        document._update(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def create_cache_servers(*, server_data):
    counter = 0
    for data in server_data:
        counter += 1
        cache.servers[data[0]] = Server(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0


async def refresh_cache_servers(*, server_data):
    counter = 0
    for data in server_data:
        counter += 1
        server = await utils.find(lambda d: d.id == data[0], cache.servers.values())
        server._update(data=data)
        if counter == 100:
            await asyncio.sleep(0)
            counter = 0