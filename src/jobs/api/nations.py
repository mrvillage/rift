from datetime import datetime

import aiohttp
from asyncpg.exceptions import DuplicateTableError

from ... import bot, jobs
from ...data import cache
from ...data.db import execute_query, execute_query_many
from ...env import APIKEY, BASEURL


async def fetch_nations():
    try:
        await execute_query(
            """
            CREATE TABLE "nationsnew" (
                "nation_id"	INTEGER NOT NULL UNIQUE,
                "nation"	TEXT,
                "leader"	TEXT,
                "continent"	INTEGER,
                "war_policy"	INTEGER,
                "domestic_policy"	INTEGER,
                "color"	INTEGER,
                "alliance_id"	INTEGER,
                "alliance"	TEXT,
                "alliance_position"	INTEGER,
                "cities"	INTEGER,
                "offensive_wars"	INTEGER,
                "defensive_wars"	INTEGER,
                "score"	REAL,
                "v_mode"	BOOLEAN,
                "v_mode_turns"	INTEGER,
                "beige_turns"	INTEGER,
                "last_active"	TEXT,
                "founded"	TEXT,
                "soldiers"	INTEGER,
                "tanks"	INTEGER,
                "aircraft"	INTEGER,
                "ships"	INTEGER,
                "missiles"	INTEGER,
                "nukes"	INTEGER,
                PRIMARY KEY("nation_id")
            );
        """
        )
    except DuplicateTableError:
        await execute_query("DROP TABLE nationsnew;")
        await execute_query(
            """
            CREATE TABLE "nationsnew" (
                "nation_id"	INTEGER NOT NULL UNIQUE,
                "nation"	TEXT,
                "leader"	TEXT,
                "continent"	INTEGER,
                "war_policy"	INTEGER,
                "domestic_policy"	INTEGER,
                "color"	INTEGER,
                "alliance_id"	INTEGER,
                "alliance"	TEXT,
                "alliance_position"	INTEGER,
                "cities"	INTEGER,
                "offensive_wars"	INTEGER,
                "defensive_wars"	INTEGER,
                "score"	REAL,
                "v_mode"	BOOLEAN,
                "v_mode_turns"	INTEGER,
                "beige_turns"	INTEGER,
                "last_active"	TEXT,
                "founded"	TEXT,
                "soldiers"	INTEGER,
                "tanks"	INTEGER,
                "aircraft"	INTEGER,
                "ships"	INTEGER,
                "missiles"	INTEGER,
                "nukes"	INTEGER,
                PRIMARY KEY("nation_id")
            );
        """
        )
    try:
        async with aiohttp.request(
            "GET", f"{BASEURL}/v2/nations/{APIKEY}/&cities=1"
        ) as response1, aiohttp.request(
            "GET", f"{BASEURL}/v2/nations/{APIKEY}/&min_cities=2"
        ) as response2:  # pylint: disable=line-too-long
            collected = datetime.utcnow()
            nations = ((await response1.json())["data"]) + (
                (await response2.json())["data"]
            )
        nations_ = [
            (
                int(i["nation_id"]),
                str(i["nation"]),
                str(i["leader"]),
                int(i["continent"]),
                int(i["war_policy"]),
                int(i["domestic_policy"]),
                int(i["color"]),
                int(i["alliance_id"]),
                str(i["alliance"]),
                int(i["alliance_position"]),
                int(i["cities"]),
                int(i["offensive_wars"]),
                int(i["defensive_wars"]),
                float(i["score"]),
                bool(i["v_mode"]),
                int(i["v_mode_turns"]),
                int(i["beige_turns"]),
                str(i["last_active"]),
                str(i["founded"]),
                int(i["soldiers"]),
                int(i["tanks"]),
                int(i["aircraft"]),
                int(i["ships"]),
                int(i["missiles"]),
                int(i["nukes"]),
            )
            for i in nations
        ]
        await execute_query_many(
            "INSERT INTO nationsnew VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25);",
            nations_,
        )  # pylint: disable=line-too-long
        await execute_query(
            """
            DROP TABLE nations;
            ALTER TABLE nationsnew RENAME TO nations;
        """
        )
        bot.nations_update = collected
    except Exception as error:  # pylint: disable=broad-except
        print("FATAL ERROR RETRIEVING NATION DATA", error)
    await jobs.target_check()
    try:
        await cache.refresh_cache_nations(nation_data=nations_)
        await cache.link_cache_cities()
        await cache.link_cache_nations()
    except UnboundLocalError:
        pass
