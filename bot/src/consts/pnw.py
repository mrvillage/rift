from __future__ import annotations

__all__ = (
    "MAX_SOLDIERS_PER_CITY",
    "MAX_TANKS_PER_CITY",
    "MAX_AIRCRAFT_PER_CITY",
    "MAX_SHIPS_PER_CITY",
    "MAX_MIL_PER_CITY",
)

MAX_SOLDIERS_PER_CITY = 15000
MAX_TANKS_PER_CITY = 1250
MAX_AIRCRAFT_PER_CITY = 75
MAX_SHIPS_PER_CITY = 15

MAX_MIL_PER_CITY = {
    "soldiers": MAX_SOLDIERS_PER_CITY,
    "tanks": MAX_TANKS_PER_CITY,
    "aircraft": MAX_AIRCRAFT_PER_CITY,
    "ships": MAX_SHIPS_PER_CITY,
}
