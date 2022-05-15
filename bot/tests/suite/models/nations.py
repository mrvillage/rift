from __future__ import annotations

import datetime
from decimal import Decimal

from src import enums, flags, models

__all__ = ("DATA",)

DATA: dict[int, models.Nation] = {
    1001: models.Nation(
        id=1001,
        alliance_id=0,
        alliance_position=enums.AlliancePosition.NO_ALLIANCE,
        name="name1001",
        leader="leader1001",
        continent=enums.Continent.NORTH_AMERICA,
        war_policy=enums.WarPolicy.TACTICIAN,
        domestic_policy=enums.DomesticPolicy.OPEN_MARKETS,
        color=enums.Color.GRAY,
        num_cities=4,
        score=Decimal("278.75"),
        flag="flag1001",
        vacation_mode_turns=274,
        beige_turns=0,
        espionage_available=True,
        last_active=datetime.datetime(
            2021, 1, 3, 12, 55, 6, tzinfo=datetime.timezone.utc
        ),
        date=datetime.datetime(2021, 1, 2, 12, 45, 37, tzinfo=datetime.timezone.utc),
        soldiers=0,
        tanks=0,
        aircraft=0,
        ships=0,
        missiles=0,
        nukes=0,
        discord_username="Nation#1001",
        turns_since_last_city=4287,
        turns_since_last_project=4287,
        projects=flags.Projects(0),
        wars_won=0,
        wars_lost=7,
        tax_id=0,
        alliance_seniority=0,
        estimated_resources=models.Resources(
            money=Decimal("0"),
            coal=Decimal("0"),
            oil=Decimal("0"),
            uranium=Decimal("0"),
            iron=Decimal("0"),
            bauxite=Decimal("0"),
            lead=Decimal("0"),
            gasoline=Decimal("0"),
            munitions=Decimal("0"),
            steel=Decimal("0"),
            aluminum=Decimal("0"),
            food=Decimal("0"),
        ),
    ),
    1002: models.Nation(
        id=1002,
        alliance_id=2001,
        alliance_position=enums.AlliancePosition.MEMBER,
        name="name1002",
        leader="leader1002",
        continent=enums.Continent.EUROPE,
        war_policy=enums.WarPolicy.TURTLE,
        domestic_policy=enums.DomesticPolicy.OPEN_MARKETS,
        color=enums.Color.GRAY,
        num_cities=3,
        score=Decimal("214.45"),
        flag="flag1002",
        vacation_mode_turns=0,
        beige_turns=0,
        espionage_available=True,
        last_active=datetime.datetime(
            2022, 5, 6, 11, 38, 10, tzinfo=datetime.timezone.utc
        ),
        date=datetime.datetime(2022, 3, 22, 20, 14, 48, tzinfo=datetime.timezone.utc),
        soldiers=15000,
        tanks=178,
        aircraft=0,
        ships=0,
        missiles=0,
        nukes=0,
        discord_username="",
        turns_since_last_city=530,
        turns_since_last_project=676,
        projects=flags.Projects(0),
        wars_won=0,
        wars_lost=0,
        tax_id=15017,
        alliance_seniority=46,
        estimated_resources=models.Resources(
            money=Decimal("0"),
            coal=Decimal("0"),
            oil=Decimal("0"),
            uranium=Decimal("0"),
            iron=Decimal("0"),
            bauxite=Decimal("0"),
            lead=Decimal("0"),
            gasoline=Decimal("0"),
            munitions=Decimal("0"),
            steel=Decimal("0"),
            aluminum=Decimal("0"),
            food=Decimal("0"),
        ),
    ),
}