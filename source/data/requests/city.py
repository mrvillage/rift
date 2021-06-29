import aiohttp
from ...ref import bot


async def get_city_build(*, city_id):
    async with aiohttp.request(
        "GET", f"https://politicsandwar.com/api/city_export.php?city_id={city_id}"
    ) as response:
        return await response.json()
