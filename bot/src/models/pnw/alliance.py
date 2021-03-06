from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs
import quarrel

from ... import cache, embeds, enums, errors, models, utils

__all__ = ("Alliance",)

if TYPE_CHECKING:
    import decimal
    from typing import Any, ClassVar

    from pnwkit.data import Alliance as PnWKitAlliance

    from ...commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Alliance:
    TABLE: ClassVar[str] = "alliances"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("color",)
    NO_UPDATE: ClassVar[tuple[str, ...]] = ("estimated_resources",)
    id: int
    name: str
    acronym: str
    score: decimal.Decimal
    color: enums.Color = attrs.field(converter=enums.Color)
    date: datetime.datetime
    accepts_members: bool
    flag: str
    forum_link: str
    discord_link: str
    wiki_link: str
    estimated_resources: models.Resources = attrs.field(
        converter=lambda x: models.Resources.from_dict(x)
    )

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Alliance:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Alliance) -> Alliance:
        ...

    @classmethod
    def from_data(cls, data: PnWKitAlliance) -> Alliance:
        if TYPE_CHECKING:
            assert isinstance(data.score, decimal.Decimal)
        return cls(
            id=data.id,
            name=data.name,
            acronym=data.acronym,
            score=data.score,
            color=getattr(enums.Color, data.color.upper()),
            date=data.date,
            accepts_members=bool(data.accept_members),
            flag=data.flag,
            forum_link=data.forum_link,
            discord_link=data.discord_link,
            wiki_link=data.wiki_link,
            estimated_resources=models.Resources(),
        )

    @property
    def applicants(self) -> set[models.Nation]:
        return {
            i
            for i in cache.nations
            if i.alliance_id == self.id
            and i.alliance_position is enums.AlliancePosition.APPLICANT
        }

    @property
    def leaders(self) -> set[models.Nation]:
        return {
            i
            for i in cache.nations
            if i.alliance_id == self.id
            and i.alliance_position is enums.AlliancePosition.LEADER
        }

    @property
    def members(self) -> set[models.Nation]:
        return {
            i
            for i in cache.nations
            if i.alliance_id == self.id and i.alliance_position.value >= 2
        }

    @property
    def rank(self) -> int:
        return (
            sorted(cache.alliances, key=lambda x: x.score, reverse=True).index(self) + 1
        )

    @property
    def treasures(self) -> set[models.Treasure]:
        return {
            i
            for i in cache.treasures
            if (n := i.nation) is not None and n.alliance_id == self.id
        }

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Alliance:
        return utils.convert_model(
            enums.ConvertType.FUZZY,
            command.interaction,
            value,
            cache.get_alliance,
            cache.alliances,
            {"name", "acronym"},
            errors.AllianceNotFoundError,
        )

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.alliance(interaction, self)
