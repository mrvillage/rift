import datetime
import json
import aiohttp
from ...data.db import execute_query
from ...env import BASEURL, APIKEY
from ... import bot


async def fetch_prices():
    try:
        async with aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=credits&key={APIKEY}"
        ) as credit, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=coal&key={APIKEY}"
        ) as coal, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=oil&key={APIKEY}"
        ) as oil, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=uranium&key={APIKEY}"
        ) as uranium, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=lead&key={APIKEY}"
        ) as lead, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=iron&key={APIKEY}"
        ) as iron, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=bauxite&key={APIKEY}"
        ) as bauxite, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=gasoline&key={APIKEY}"
        ) as gasoline, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=munitions&key={APIKEY}"
        ) as munitions, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=steel&key={APIKEY}"
        ) as steel, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=aluminum&key={APIKEY}"
        ) as aluminum, aiohttp.request(
            "GET", f"{BASEURL}/tradeprice/?resource=food&key={APIKEY}"
        ) as food:  # pylint: disable=line-too-long
            collected = datetime.datetime.utcnow()
            resources = (
                json.dumps(await credit.json()),
                json.dumps(await coal.json()),
                json.dumps(await oil.json()),
                json.dumps(await uranium.json()),
                json.dumps(await lead.json()),
                json.dumps(await iron.json()),
                json.dumps(await bauxite.json()),
                json.dumps(await gasoline.json()),
                json.dumps(await munitions.json()),
                json.dumps(await steel.json()),
                json.dumps(await aluminum.json()),
                json.dumps(await food.json()),
            )
        await execute_query(
            "INSERT INTO prices (datetime, credit, coal, oil, uranium, lead, iron, bauxite, gasoline, munitions, steel, aluminum, food) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13);",
            str(collected),
            *resources,
        )  # pylint: disable=line-too-long
        bot.prices_update = collected
    except Exception as error:  # pylint: disable=broad-except
        print("FATAL ERROR RETRIEVING PRICE DATA", error)
