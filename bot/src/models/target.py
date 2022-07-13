from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import lang
import quarrel

from .. import consts, enums, strings, utils

__all__ = ("Target",)

if TYPE_CHECKING:
    from .. import flags, models


@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Target:
    nation: models.Nation
    rating: float
    attributes: tuple[TargetAttribute]

    def build_embed_field(self) -> quarrel.EmbedField:
        return utils.embed_field(
            strings.target_field_name(self.nation, self.rating),
            strings.target_field_value(self),
        )

    @classmethod
    def rate_target(
        cls,
        count: flags.TargetFindCounting,
        rater: models.TargetRater,
        attacker: models.Nation,
        defender: models.Nation,
    ) -> Target:
        attributes: list[TargetAttribute] = []
        for attr in attrs.fields(type(rater)):
            if getattr(count, attr.name, None):
                attr_rater: str = getattr(rater, attr.name)
                if attr_rater:
                    attributes.append(
                        TargetAttribute(
                            name=attr.name,
                            value=TargetAttribute.get_value(attr.name, defender),
                            rating=float(
                                utils.evaluate_in_default_scope(
                                    lang.parse_expression(attr_rater),
                                    nation=attacker,
                                    target=defender,
                                )
                            ),
                        )
                    )
        return cls(
            nation=defender,
            rating=sum(attr.rating for attr in attributes),
            attributes=tuple(attributes),
        )


@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetAttribute:
    name: str
    value: str
    rating: float

    @classmethod
    def get_value(cls, attr: str, nation: models.Nation) -> str:
        if attr in {"soldiers", "tanks", "aircraft", "ships"}:
            value = getattr(nation, attr)
            return f"{value:,} ({value / (consts.MAX_MIL_PER_CITY[attr] * nation.num_cities):,.2%})"
        elif attr == "activity":
            return strings.datetime_mention(
                nation.last_active, enums.TimestampStyle.SHORT_DATETIME
            )
        elif attr == "infrastructure":
            return f"{nation.average_infrastructure:,.2f}"
        else:
            return str(getattr(nation, attr))
