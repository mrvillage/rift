import datetime
import json
import aiohttp
import asyncio
from ...data.db import execute_query, execute_query_many
from ...env import BASEURL, APIKEY
from ... import jobs
from ... import bot
from ...data import cache
from asyncpg.exceptions import DuplicateTableError


async def fetch_alliances():
    try:
        await execute_query(f"""
            CREATE TABLE "alliancesnew" (
                "id"	INTEGER,
                "founddate"	TEXT,
                "name"	TEXT,
                "acronym"	TEXT,
                "color"	TEXT,
                "rank"	INTEGER,
                "members"	INTEGER,
                "score"	REAL,
                "leaderids"	TEXT,
                "officerids"	TEXT,
                "heirids"	TEXT,
                "avgscore"	REAL,
                "flagurl"	TEXT,
                "forumurl"	TEXT,
                "ircchan"	TEXT,
                PRIMARY KEY("id")
            );
            """)
    except DuplicateTableError:
        await execute_query(f"DROP TABLE alliancesnew;")
        await execute_query(f"""
            CREATE TABLE "alliancesnew" (
                "id"	INTEGER,
                "founddate"	TEXT,
                "name"	TEXT,
                "acronym"	TEXT,
                "color"	TEXT,
                "rank"	INTEGER,
                "members"	INTEGER,
                "score"	REAL,
                "leaderids"	TEXT,
                "officerids"	TEXT,
                "heirids"	TEXT,
                "avgscore"	REAL,
                "flagurl"	TEXT,
                "forumurl"	TEXT,
                "ircchan"	TEXT,
                PRIMARY KEY("id")
            );
            """)
    try:
        async with aiohttp.request("GET", f"{BASEURL}/alliances/?key={APIKEY}") as response:
            collected = datetime.datetime.utcnow()
            print("Alliances", collected)
            alliances = json.loads(await response.text())
            alliances_ = [(
                int(i['id']),
                i['founddate'],
                i['name'],
                i['acronym'],
                i['color'],
                int(i['rank']),
                int(i['members']) if 'members' in i else None,
                float(i['score']) if 'score' in i else None,
                str([int(j) for j in i['leaderids']]
                    ) if 'leaderids' in i else None,
                str([int(j) for j in i['officerids']]
                    ) if 'officerids' in i else None,
                str([int(j) for j in i['heirids']]
                    ) if 'heirids' in i else None,
                float(i['avgscore']),
                str(i['flagurl']) if not i['flagurl'] == "" else None,
                str(i['forumurl']) if not i['forumurl'] == "" else None,
                str(i['ircchan']) if not i['ircchan'] == "" else None,
            ) for i in alliances['alliances']]
            # await rift.execute_query_many( "INSERT INTO alliancesnew VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",alliances_)
            for i, alliance in enumerate(alliances_):
                await asyncio.sleep(0)
                await execute_query("INSERT INTO alliancesnew (id, founddate, name, acronym, color, rank, members, score, leaderids, officerids, heirids, avgscore, flagurl, forumurl, ircchan) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);", *alliance)
        await execute_query(f"""
            DROP TABLE alliances;
            ALTER TABLE alliancesnew RENAME TO alliances;
        """)
        bot.alliances_update = collected
    except Exception as error:
        print("FATAL ERROR RETRIEVING ALLIANCE DATA", error)
    try:
        await cache.refresh_cache_alliances(alliance_data=alliances_)
    except UnboundLocalError:
        pass
