from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import consts, enums, models, strings, utils

__all__ = ("not_found_error", "nation")

if TYPE_CHECKING:
    from typing import Optional


def not_found_error(
    user: quarrel.User | quarrel.Member,
    name: str,
    value: Optional[str],
    infer: bool = False,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.not_found(name, value, infer),
        color=consts.ERROR_EMBED_COLOR,
    )


def nation(user: quarrel.User | quarrel.Member, nation: models.Nation) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        color=consts.INFO_EMBED_COLOR,
        footer_text=strings.model_created("Nation"),
        timestamp=nation.date,
        description=strings.nation_linked_to(nation),
        fields=[
            utils.embed_field(
                name="Nation ID", value=strings.nation_link(nation, nation.id)
            ),
            utils.embed_field(
                name="Name", value=strings.nation_link(nation, nation.name)
            ),
            utils.embed_field(
                name="Leader", value=strings.nation_link(nation, nation.leader)
            ),
            utils.embed_field(
                name="War Policy", value=strings.enum_name(nation.war_policy)
            ),
            utils.embed_field(
                name="Domestic Policy",
                value=strings.enum_name(nation.domestic_policy),
            ),
            utils.embed_field(
                name="Continent",
                value=strings.enum_name(nation.continent),
            ),
            utils.embed_field(
                name="Color",
                value=strings.enum_name(nation.color)
                if nation.color is not enums.Color.BEIGE
                else strings.color_and_beige_turns(nation.beige_turns),
            ),
            utils.embed_field(
                name="Alliance", value=strings.alliance_link_using_name(nation.alliance)
            ),
            utils.embed_field(
                name="Alliance Position",
                value=strings.enum_name(nation.alliance_position),
            ),
            utils.embed_field(
                name="Cities",
                value=strings.city_manager_link(nation, nation.num_cities),
            ),
            utils.embed_field(
                name="Score",
                value=f"{nation.score:.2f}",
            ),
            utils.embed_field(
                name="Vacation Mode",
                value=strings.vacation_mode(nation.vacation_mode_turns),
            ),
            utils.embed_field(
                name="Soldiers",
                value=f"{nation.soldiers:,}/{nation.num_cities * consts.MAX_SOLDIERS_PER_CITY}",
            ),
            utils.embed_field(
                name="Tanks",
                value=f"{nation.tanks:,}/{nation.num_cities * consts.MAX_TANKS_PER_CITY}",
            ),
            utils.embed_field(
                name="Aircraft",
                value=f"{nation.aircraft:,}/{nation.num_cities * consts.MAX_AIRCRAFT_PER_CITY}",
            ),
            utils.embed_field(
                name="Ships",
                value=f"{nation.ships:,}/{nation.num_cities * consts.MAX_SHIPS_PER_CITY}",
            ),
            utils.embed_field(
                name="Missiles",
                value=f"{nation.missiles:,}",
            ),
            utils.embed_field(
                name="Nukes",
                value=f"{nation.nukes:,}",
            ),
            utils.embed_field(
                name="Average Infrastructure",
                value=f"{nation.average_infrastructure:.2f}",
            ),
            utils.embed_field(
                name="Average Land",
                value=f"{nation.average_land:.2f}",
            ),
        ],
    )
