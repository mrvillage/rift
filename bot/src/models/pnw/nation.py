from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import cache, enums, flags, utils

__all__ = ("Nation",)

if TYPE_CHECKING:
    import datetime
    import decimal
    from typing import ClassVar

    from pnwkit.data import Nation as PnWKitNation

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
    projects: flags.Projects = attrs.field(converter=flags.Projects)
    wars_won: int
    wars_lost: int
    tax_id: int
    alliance_seniority: int
    estimated_resources: models.Resources

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: NationData) -> Nation:
        ...

    def to_dict(self) -> NationData:
        ...

    def update(self, data: Nation) -> Nation:
        ...

    @classmethod
    def from_data(cls, data: PnWKitNation) -> Nation:
        if TYPE_CHECKING:
            assert isinstance(data.score, decimal.Decimal)
        alliance_position = getattr(
            enums.AlliancePosition,
            data.alliance_position
            if data.alliance_position != "NOALLIANCE"
            else "NO_ALLIANCE",
        )
        return cls(
            id=int(data.id),
            alliance_id=int(data.alliance_id),
            alliance_position=getattr(enums.AlliancePosition, alliance_position),
            name=data.nation_name,
            leader=data.leader_name,
            # as is a python keyword so cannot be used as an attribute name
            continent=getattr(enums.Continent, data.continent)
            if data.continent != "as"
            else enums.Continent.ASIA,
            war_policy=getattr(enums.WarPolicy, data.warpolicy.upper()),
            domestic_policy=getattr(
                enums.DomesticPolicy, data.dompolicy.upper().replace(" ", "_")
            ),
            color=getattr(enums.Color, data.color.upper()),
            num_cities=data.num_cities,
            score=data.score,
            flag=data.flag,
            v_mode=bool(data.vmode),
            beige_turns=data.beigeturns,
            espionage_available=data.espionage_available,
            last_active=datetime.datetime.fromisoformat(data.last_active),
            date=datetime.datetime.fromisoformat(data.date),
            soldiers=data.soldiers,
            tanks=data.tanks,
            aircraft=data.aircraft,
            ships=data.ships,
            missiles=data.missiles,
            nukes=data.nukes,
            turns_since_last_city=data.turns_since_last_city,
            turns_since_last_project=data.turns_since_last_project,
            # attrs will convert the type
            projects=data.project_bits,  # type: ignore
            wars_won=data.wars_won,
            wars_lost=data.wars_lost,
            tax_id=int(data.tax_id),
            alliance_seniority=data.alliance_seniority,
            estimated_resources=models.Resources(),
        )
