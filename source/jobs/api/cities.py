import datetime
import aiohttp
from asyncpg.exceptions import DuplicateTableError
from ...data.db import execute_query, execute_query_many
from ...env import BASEURL, APIKEY
from ... import bot
from ...data import cache


async def fetch_cities():
    try:
        await execute_query("""
            CREATE TABLE "citiesnew" (
                "id"	INTEGER NOT NULL UNIQUE,
                "nation_id" INTEGER,
                "city_name" TEXT,
                "capital" BOOLEAN,
                "infrastructure" REAL,
                "maxinfra" REAL,
                "land" REAL,
                PRIMARY KEY("id")
            );
            """)
    except DuplicateTableError:
        await execute_query("DROP TABLE citiesnew;")
        await execute_query("""
            CREATE TABLE "citiesnew" (
                "id"	INTEGER NOT NULL UNIQUE,
                "nation_id" INTEGER,
                "city_name" TEXT,
                "capital" BOOLEAN,
                "infrastructure" REAL,
                "maxinfra" REAL,
                "land" REAL,
                PRIMARY KEY("id")
            );
            """)
    try:
        async with aiohttp.request("GET", f"{BASEURL}/all-cities/key={APIKEY}") as response:
            collected = datetime.datetime.utcnow()
            cities = await response.json()
            cities_ = [(
                int(i['city_id']),
                int(i['nation_id']),
                i['city_name'],
                bool(int(i['capital'])),
                float(i['infrastructure']),
                float(i['maxinfra']),
                float(i['land'])
            ) for i in cities['all_cities']]
            await execute_query_many("INSERT INTO citiesnew (id, nation_id, city_name, capital, infrastructure, maxinfra, land) VALUES ($1, $2, $3, $4, $5, $6, $7);", cities_)  # pylint: disable=line-too-long
        await execute_query("""
            DROP TABLE cities;
            ALTER TABLE citiesnew RENAME TO cities;
        """)
        bot.cities_update = collected
    except Exception as error:  # pylint: disable=broad-except
        print("FATAL ERROR RETRIEVING CITY DATA", error)
    try:
        await cache.refresh_cache_cities(city_data=cities_)
    except UnboundLocalError:
        pass
