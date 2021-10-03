from __future__ import annotations

from typing import Union

import aiohttp

from ..data.classes import Nation
from ..errors import InvalidSpyResponseError, SpiesNotFoundError

__all__ = ("calculate_spies",)


async def spies_request(*, target_id: int, num_spies: int, safety: int) -> bool:
    """
    Returns True if odds are greater than 50%, returns False if odds are less than 50%
    """
    async with aiohttp.request(
        "GET",
        f"https://politicsandwar.com/war/espionage_get_odds.php?id1=251584&id2={target_id}&id3=0&id4={safety}&id5={num_spies}",
    ) as response:
        text = await response.text()
        if "Lower" in text:
            return False
        elif "Greater" in text:
            return True
        raise InvalidSpyResponseError(text)


async def get_spies(target: Union[int, Nation], safety: int = 1) -> float:
    if isinstance(target, int):
        target = await Nation.fetch(target)
    fetch_amount = 30
    if await spies_request(target_id=target.id, num_spies=fetch_amount, safety=safety):
        fetch_amount -= 5
        last = True
    else:
        fetch_amount += 5
        last = False
    while True:
        new = await spies_request(
            target_id=target.id, num_spies=fetch_amount, safety=safety
        )
        if last != new:
            break
        if new:
            fetch_amount -= 5
            last = True
        else:
            fetch_amount += 5
            last = False
        if fetch_amount < 0 or fetch_amount > 60:
            raise SpiesNotFoundError(f"Could not find any spies for {target.id}")
    if new:
        while True:
            second = await spies_request(
                target_id=target.id, num_spies=fetch_amount, safety=safety
            )
            if new != second:
                break
            fetch_amount -= 1
            if fetch_amount < 0 or fetch_amount > 60:
                raise SpiesNotFoundError(f"Could not find any spies for {target.id}")
    else:
        while True:
            second = await spies_request(
                target_id=target.id, num_spies=fetch_amount, safety=safety
            )
            if new != second:
                break
            fetch_amount += 1
            if fetch_amount < 0 or fetch_amount > 60:
                raise SpiesNotFoundError(f"Could not find any spies for {target.id}")
    odds = 50
    if target.war_policy == "Arcane":
        mod = 0.82
    elif target.war_policy == "Tactician":
        mod = 0.88
    else:
        mod = 1
    num = (((100 * fetch_amount) / ((odds * mod) - (25 * safety))) - 1) / 3
    num = num if num > 0 else num * -1
    if num < 30:
        if target.war_policy == "Arcane":
            mod = 0.8
        elif target.war_policy == "Tactician":
            mod = 0.9
        else:
            mod = 1
            if num > 20:
                odds = 51 if second else 49
        num = (((100 * fetch_amount) / ((odds * mod) - (25 * safety))) - 1) / 3
        return num if num > 0 else num * -1
    return num


async def calculate_spies(nation: Nation) -> int:
    safety_levels = (
        (3, 2, 1) if nation.war_policy in {"Tactician", "Arcane"} else (1, 2, 3)
    )
    try:
        num = await get_spies(nation, safety_levels[0])
    except SpiesNotFoundError:
        try:
            num = await get_spies(nation, safety_levels[1])
        except SpiesNotFoundError:
            try:
                num = await get_spies(nation, safety_levels[2])
            except SpiesNotFoundError:
                return 0
    return int(round(num, 0)) if num > 30 else int(num)
