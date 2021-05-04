from ..errors import ConvertError  # pylint: disable=relative-beyond-top-level
from asyncio import sleep

color_map = ("Beige", "Gray", "Lime", "Green", "White", "Brown", "Maroon",
             "Purple", "Blue", "Red", "Orange", "Olive", "Aqua", "Black", "Yellow", "Pink")


def get_color(id, *, beige_turns=None):
    return color_map[id]
    # if id == 0:
    #     return f"{color_map[id]} ({beige_turns} Turns)"
    # else:
    #     return color_map[id]


domestic_policy_map = ("Manifest Destiny", "Open Markets",
                       "Technological Advancement", "Imperialism", "Urbanization")


def get_domestic_policy(id):
    return domestic_policy_map[id-1]


war_policy_map = ("Attrition", "Turtle", "Blitzkrieg", "Fortress",
                  "Moneybags", "Pirate", "Tactician", "Guardian", "Covert", "Arcane")


def get_war_policy(id):
    return war_policy_map[id-1]


alliance_position_map = ("None", "Applicant", "Member",
                         "Officer", "Heir", "Leader")


def get_alliance_position(id):
    return alliance_position_map[id]


continent_map = ("North America", "South America", "Europe",
                 "Africa", "Asia", "Australia", "Antarctica")


def get_continent(id):
    return continent_map[id-1]


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
    return True if value.lower() in {"true", "yes", "approve", "go", "accept"} else False if value.lower() in {"false", "no", "deny"} else 1/0


async def get_command_signature(ctx):
    return f"{ctx.bot.command_prefix}{ctx.command.qualified_name} {ctx.command.signature}"

get_command_help = get_command_signature
