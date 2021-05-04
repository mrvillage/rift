import datetime
import json
import aiohttp
from ...data.db import execute_query, execute_query_many
from ...env import BASEURL, APIKEY
from ... import jobs
from ... import bot
from ...data import cache
from asyncpg.exceptions import DuplicateTableError


async def fetch_cities():
    try:
        await execute_query(f"""
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
        await execute_query(f"DROP TABLE citiesnew;")
        await execute_query(f"""
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
            print("Cities", collected)
            cities = json.loads(await response.text())
            cities_ = [(
                int(i['city_id']),
                int(i['nation_id']),
                i['city_name'],
                bool(int(i['capital'])),
                float(i['infrastructure']),
                float(i['maxinfra']),
                float(i['land'])
            ) for i in cities['all_cities']]
            # await rift.execute_query_many( "INSERT INTO alliancesnew VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",alliances_)
            await execute_query_many("INSERT INTO citiesnew (id, nation_id, city_name, capital, infrastructure, maxinfra, land) VALUES ($1, $2, $3, $4, $5, $6, $7);", cities_)
        await execute_query(f"""
            DROP TABLE cities;
            ALTER TABLE citiesnew RENAME TO cities;
        """)
        bot.cities_update = collected
    except Exception as error:
        print("FATAL ERROR RETRIEVING CITY DATA", error)
    try:
        await cache.refresh_cache_cities(city_data=cities_)
    except UnboundLocalError:
        pass
