from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils
from ...cache import cache

__all__ = ("Nation",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from ... import models
    from ...types.models.pnw.nation import Nation as NationData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Nation:
    TABLE: ClassVar[str] = "nations"
    id: int
    alliance_id: int
    alliance_position: enums.AlliancePosition = attrs.field(
        converter=enums.AlliancePosition
    )
    name: str
    leader: str
    continent: enums.Continent = attrs.field(converter=enums.Continent)
    war_policy: enums.WarPolicy
    domestic_policy: enums.DomesticPolicy = attrs.field(converter=enums.DomesticPolicy)
    color: models.Color = attrs.field(
        converter=lambda x: cache.get_color(enums.Color(x))
    )
    num_cities: int
    score: decimal.Decimal
    flag: str
    v_mode: bool
    beige_turns: int
    espionage_available: bool
    last_active: datetime.datetime
    date: datetime.datetime
    soldiers: int
    tanks: int
    aircraft: int
    ships: int
    missiles: int
    nukes: int
    turns_since_last_city: int
    turns_since_last_project: int
    projects: int
    wars_won: int
    wars_lost: int
    tax_id: int
    alliance_seniority: int
    estimated_resources: models.Resources

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: NationData) -> Nation:
        ...
