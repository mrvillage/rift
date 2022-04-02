from __future__ import annotations

import enum

__all__ = (
    "AlliancePosition",
    "BankrecParticipantType",
    "BountyType",
    "Color",
    "Continent",
    "DomesticPolicy",
    "Resource",
    "TradeAction",
    "TradeType",
    "TreatyType",
    "WarAttackType",
    "WarPolicy",
    "WarType",
)


class AlliancePosition(enum.Enum):
    NO_ALLIANCE = 0
    APPLICANT = 1
    MEMBER = 2
    OFFICER = 3
    HEIR = 4
    LEADER = 5

    # pnw aliases
    NOALLIANCE = 0


class BankrecParticipantType(enum.Enum):
    NATION = 1
    ALLIANCE = 2
    TAXES = 3


class BountyType(enum.Enum):
    ORDINARY = 0
    ATTRITION = 1
    RAID = 2
    NUCLEAR = 3


class Color(enum.Enum):
    BEIGE = 0
    GRAY = 1
    LIME = 2
    GREEN = 3
    WHITE = 4
    BROWN = 5
    MAROON = 6
    PURPLE = 7
    BLUE = 8
    RED = 9
    ORANGE = 10
    OLIVE = 11
    AQUA = 12
    BLACK = 13
    YELLOW = 14
    PINK = 15


class Continent(enum.Enum):
    NORTH_AMERICA = 1
    SOUTH_AMERICA = 2
    EUROPE = 3
    AFRICA = 4
    ASIA = 5
    AUSTRALIA = 6
    ANTARCTICA = 7

    # pnw aliases
    na = 1
    sa = 2
    eu = 3
    af = 4
    au = 6
    an = 7


class DomesticPolicy(enum.Enum):
    MANIFEST_DESTINY = 1
    OPEN_MARKETS = 2
    TECHNOLOGICAL_ADVANCEMENT = 3
    IMPERIALISM = 4
    URBANIZATION = 5
    RAPID_EXPANSION = 6


class Resource(enum.Enum):
    MONEY = 0
    COAL = 1
    OIL = 2
    URANIUM = 3
    IRON = 4
    BAUXITE = 5
    LEAD = 6
    GASOLINE = 7
    MUNITIONS = 8
    STEEL = 9
    ALUMINUM = 10
    FOOD = 11


class TradeAction(enum.Enum):
    BUY = 0
    SELL = 1


class TradeType(enum.Enum):
    GLOBAL = 0
    PERSONAL = 1
    ALLIANCE = 2


class TreatyType(enum.Enum):
    MDP = 0
    MDOAP = 1
    ODP = 2
    ODOAP = 3
    PROTECTORATE = 4
    PIAT = 5
    NAP = 6


class WarAttackType(enum.Enum):
    AIR_V_INFRA = 0
    AIR_V_SOLDIERS = 1
    AIR_V_TANKS = 2
    AIR_V_MONEY = 3
    AIR_V_SHIPS = 4
    AIR_V_AIR = 5
    GROUND = 6
    MISSILE = 7
    MISSILE_FAIL = 8
    NUKE = 9
    NUKE_FAIL = 10
    NAVAL = 11
    FORTIFY = 12
    PEACE = 13
    VICTORY = 14
    ALLIANCE_LOOT = 15

    # pnw aliases
    AIRVINFRA = 0
    AIRVSOLDIERS = 1
    AIRVTANKS = 2
    AIRVMONEY = 3
    AIRVSHIPS = 4
    AIRVAIR = 5
    MISSILEFAIL = 8
    NUKEFAIL = 10
    ALLIANCELOOT = 15


class WarPolicy(enum.Enum):
    ATTRITION = 1
    TURTLE = 2
    BLITZKRIEG = 3
    FORTRESS = 4
    MONEYBAGS = 5
    PIRATE = 6
    TACTICIAN = 7
    GUARDIAN = 8
    COVERT = 9
    ARCANE = 10


class WarType(enum.Enum):
    ORDINARY = 0
    ATTRITION = 1
    RAID = 2
