from __future__ import annotations

import datetime
from decimal import Decimal

from src import enums, models

__all__ = ("DATA",)

DATA: dict[int, models.Alliance] = {
    2001: models.Alliance(
        id=2001,
        name="alliance2001",
        acronym="a2001",
        score=Decimal("446.94"),
        color=enums.Color.BROWN,
        date=datetime.datetime(2017, 5, 10, 18, 55, 22, tzinfo=datetime.timezone.utc),
        accepts_members=True,
        flag="flag2001",
        forum_link="",
        discord_link="",
        wiki_link="",
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
    )
}
