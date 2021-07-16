import random
import string
from asyncio import sleep

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


def get_color(color_id):
    return color_map[color_id]
    # if id == 0:
    #     return f"{color_map[id]} ({beige_turns} Turns)"
    # else:
    #     return color_map[id]


def get_color_id(name):
    return color_map.index(name)


domestic_policy_map = (
    "Manifest Destiny",
    "Open Markets",
    "Technological Advancement",
    "Imperialism",
    "Urbanization",
)


def get_domestic_policy(policy_id):
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


def get_war_policy(policy_id):
    return war_policy_map[policy_id - 1]


alliance_position_map = ("None", "Applicant", "Member", "Officer", "Heir", "Leader")


def get_alliance_position(position_id):
    return alliance_position_map[position_id]


def get_alliance_position_id(position):
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


def get_continent(continent_id):
    return continent_map[continent_id - 1]


async def find(predicate, iterable):
    counter = 0
    for element in iterable:
        counter += 1
        if predicate(element):
            return element
        if counter == 100:
            await sleep(0)
            counter = 0


async def convert_bool(value):
    from ...errors import BoolError

    if value.lower() in {"true", "yes", "approve", "go", "accept"}:
        return True
    if value.lower() in {"false", "no", "deny"}:
        return False
    raise BoolError


async def get_command_signature(ctx):
    return f"{(await ctx.bot.get_guild_prefixes(ctx.guild.id))[0]}{ctx.command.qualified_name} {ctx.command.signature}"


get_command_help = get_command_signature


async def generate_code(length=16):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


async def convert_link(search):
    from ...errors import LinkError

    if "politicsandwar" in search:
        return search.strip(string.ascii_letters + ".:/=")
    raise LinkError


async def convert_number(num):
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


async def check_resource(arg):
    return arg.lower() in resources
