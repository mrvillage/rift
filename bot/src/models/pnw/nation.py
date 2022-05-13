from __future__ import annotations

import contextlib
import datetime
import decimal
from typing import TYPE_CHECKING

import attrs
import quarrel

from ... import cache, components, embeds, enums, errors, flags, models, utils

__all__ = ("Nation",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    from pnwkit.data import Nation as PnWKitNation

    from ...commands.common import CommonSlashCommand
    from ...types.models.pnw.nation import Nation as NationData
    from ...types.quarrel import MemberOrUser


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Nation:
    TABLE: ClassVar[str] = "nations"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = (
        "alliance_position",
        "continent",
        "war_policy",
        "domestic_policy",
        "color",
    )
    NO_UPDATE: ClassVar[tuple[str, ...]] = ("estimated_resources",)
    id: int
    alliance_id: int
    alliance_position: enums.AlliancePosition = attrs.field(
        converter=enums.AlliancePosition
    )
    name: str
    leader: str
    continent: enums.Continent = attrs.field(converter=enums.Continent)
    war_policy: enums.WarPolicy = attrs.field(converter=enums.WarPolicy)
    domestic_policy: enums.DomesticPolicy = attrs.field(converter=enums.DomesticPolicy)
    # TODO: When color data is available, convert to models.Color instead
    color: enums.Color = attrs.field(converter=enums.Color)
    num_cities: int
    score: decimal.Decimal
    flag: str
    vacation_mode_turns: int
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
    discord_username: str
    turns_since_last_city: int
    turns_since_last_project: int
    projects: flags.Projects = attrs.field(converter=flags.Projects)
    wars_won: int
    wars_lost: int
    tax_id: int
    alliance_seniority: int
    estimated_resources: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )

    async def save(self, insert: bool = False) -> None:
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
            data.alliance_position.name
            if data.alliance_position.name != "NOALLIANCE"
            else "NO_ALLIANCE",
        )
        return cls(
            id=data.id,
            alliance_id=data.alliance_id,
            alliance_position=alliance_position,
            name=data.nation_name,
            leader=data.leader_name,
            # as is a python keyword so cannot be used as an attribute name
            continent=getattr(enums.Continent, data.continent)
            if data.continent != "as"
            else enums.Continent.ASIA,
            war_policy=getattr(enums.WarPolicy, data.war_policy.name),
            domestic_policy=getattr(enums.DomesticPolicy, data.domestic_policy.name),
            color=getattr(enums.Color, data.color.upper()),
            num_cities=data.num_cities,
            score=data.score,
            flag=data.flag,
            vacation_mode_turns=data.vacation_mode_turns,
            beige_turns=data.beige_turns,
            espionage_available=data.espionage_available,
            last_active=data.last_active,
            date=data.date,
            soldiers=data.soldiers,
            tanks=data.tanks,
            aircraft=data.aircraft,
            ships=data.ships,
            missiles=data.missiles,
            nukes=data.nukes,
            discord_username=data.discord,
            turns_since_last_city=data.turns_since_last_city,
            turns_since_last_project=data.turns_since_last_project,
            # attrs will convert the type
            projects=data.project_bits,  # type: ignore
            wars_won=data.wars_won,
            wars_lost=data.wars_lost,
            tax_id=data.tax_id,
            alliance_seniority=data.alliance_seniority,
            estimated_resources=models.Resources(),
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    @property
    def alliance(self) -> Optional[models.Alliance]:
        return cache.get_alliance(self.alliance_id)

    @property
    def average_infrastructure(self) -> decimal.Decimal:
        return (
            sum((i.infrastructure for i in self.cities), start=decimal.Decimal())
            / self.num_cities
        )

    @property
    def average_land(self) -> decimal.Decimal:
        return (
            sum((i.land for i in self.cities), start=decimal.Decimal())
            / self.num_cities
        )

    @property
    def cities(self) -> set[models.City]:
        return {i for i in cache.cities if i.nation_id == self.id}

    @property
    def user(self) -> Optional[models.User]:
        return cache.get_user(self.id)

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Nation:
        with contextlib.suppress(ValueError):
            nation = cache.get_nation(utils.convert_int(value))
            if nation is not None:
                return nation
        raise errors.NationNotFoundError(command.interaction, value)

    def build_embed(self, user: MemberOrUser) -> quarrel.Embed:
        return embeds.nation(user, self)

    def build_grid(self) -> components.NationGrid:
        return components.NationGrid(self)
