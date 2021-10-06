from __future__ import annotations

import random
import string
from typing import TYPE_CHECKING, Dict, Mapping, Union

from ...ref import RiftContext

__all__ = (
    "get_color",
    "get_color_id",
    "get_domestic_policy",
    "get_war_policy",
    "get_alliance_position",
    "get_alliance_position_id",
    "get_continent",
    "convert_bool",
    "get_command_signature",
    "generate_code",
    "convert_link",
    "convert_number",
    "convert_int",
    "check_resource",
    "parse_time",
    "convert_seconds_to_text",
)

color_map = (
    "Beige",
    "Gray",
    "Lime",
    "Green",
    "White",
    "Brown",
    "Maroon",
    "Purple",
    "Blue",
    "Red",
    "Orange",
    "Olive",
    "Aqua",
    "Black",
    "Yellow",
    "Pink",
)


def get_color(color_id: int) -> str:
    return color_map[color_id]
    # if id == 0:
    #     return f"{color_map[id]} ({beige_turns} Turns)"
    # else:
    #     return color_map[id]


def get_color_id(name: str) -> int:
    return color_map.index(name)


domestic_policy_map = (
    "Manifest Destiny",
    "Open Markets",
    "Technological Advancement",
    "Imperialism",
    "Urbanization",
)


def get_domestic_policy(policy_id: int) -> str:
    return domestic_policy_map[policy_id - 1]


war_policy_map = (
    "Attrition",
    "Turtle",
    "Blitzkrieg",
    "Fortress",
    "Moneybags",
    "Pirate",
    "Tactician",
    "Guardian",
    "Covert",
    "Arcane",
)


def get_war_policy(policy_id: int) -> str:
    return war_policy_map[policy_id - 1]


alliance_position_map = ("None", "Applicant", "Member", "Officer", "Heir", "Leader")


def get_alliance_position(position_id: int) -> str:
    return alliance_position_map[position_id]


def get_alliance_position_id(position: str) -> int:
    return alliance_position_map.index(position)


continent_map = (
    "North America",
    "South America",
    "Europe",
    "Africa",
    "Asia",
    "Australia",
    "Antarctica",
)


def get_continent(continent_id: int) -> str:
    return continent_map[continent_id - 1]


def convert_bool(value: str) -> bool:
    from ...errors import BoolError

    if value.lower() in {"true", "yes", "approve", "go", "accept"}:
        return True
    if value.lower() in {"false", "no", "deny"}:
        return False
    raise BoolError


def get_command_signature(ctx: RiftContext) -> str:
    if TYPE_CHECKING:
        assert ctx.command is not None
    return f"?{ctx.command.qualified_name} {ctx.command.signature}"  # type: ignore


get_command_help = get_command_signature


def generate_code(length: int = 16) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def convert_link(search: str) -> str:
    from ...errors import LinkError

    if "politicsandwar" in search:
        return search.strip(string.ascii_letters + ".:/=")
    raise LinkError


def convert_number(num: str) -> Union[int, float]:
    num = "".join(i for i in num if i in string.digits or i == ".")
    if num.count(".") > 1:
        last = num.rfind(".")
        beginning = num[:last]
        end = num[last:]
        return float(beginning.replace(".", "") + end)
    elif num.count(".") == 1:
        return float(num)
    else:
        return int(num)


def convert_int(num: str) -> int:
    return int(convert_number(num))


resources = (
    "credit",
    "credits",
    "coal",
    "oil",
    "uranium",
    "lead",
    "iron",
    "bauxite",
    "gasoline",
    "munitions",
    "steel",
    "aluminum",
    "food",
    "money",
)


def check_resource(arg: str) -> bool:
    return arg.lower() in resources


durations = {"w": "weeks", "d": "days", "h": "hours", "m": "minutes", "s": "seconds"}


def parse_time(time: str) -> Mapping[str, int]:
    time = time.lower().replace(",", "").replace(".", "")
    w = time.index("w") if "w" in time else -2
    d = time.index("d") if "d" in time else -2
    h = time.index("h") if "h" in time else -2
    m = time.index("m") if "m" in time else -2
    s = time.index("s") if "s" in time else -2
    indexes = {"start": -1, "w": w, "d": d, "h": h, "m": m, "s": s}
    indexes = {key: value for key, value in indexes.items() if value != -2}
    keys = sorted(indexes, key=lambda x: indexes[x])
    if len(keys) == 1:
        raise ValueError("No valid time was specified")
    kwargs: Dict[str, int] = {}
    for index in range(1, len(keys)):
        duration = durations[keys[index]]
        value = time[indexes[keys[index - 1]] + 1 : indexes[keys[index]]]
        kwargs[duration] = int(value)
    return kwargs


def convert_seconds_to_text(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:,.2f} seconds"
    minutes = int(seconds // 60)
    seconds -= minutes * 60
    if minutes < 60:
        return f"{minutes} minutes, and {seconds:,.2f} seconds"
    hours = int(minutes // 60)
    minutes -= hours * 60
    if hours < 24:
        return f"{hours} hours, {minutes} minutes, and {seconds:,.2f} seconds"
    days = int(hours // 24)
    hours -= days * 24
    if days < 7:
        return (
            f"{days} days, {hours} hours, {minutes} minutes, and {seconds:,.2f} seconds"
        )
    weeks = int(days // 7)
    days -= weeks * 7
    return f"{weeks} weeks, {days} days, {hours} hours, {minutes} minutes, and {seconds:,.2f} seconds"
