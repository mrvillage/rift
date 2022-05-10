from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import quarrel

from .. import cache, consts, enums, models, strings, utils

__all__ = ("not_found_error", "nation_not_in_alliance_error", "nation", "alliance")

if TYPE_CHECKING:
    from typing import Optional

    from ..types.quarrel import MemberOrUser


def not_found_error(
    user: MemberOrUser,
    name: str,
    value: Optional[str],
    infer: bool = False,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.not_found(name, value, infer),
        color=consts.ERROR_EMBED_COLOR,
    )


def nation_not_in_alliance_error(
    user: MemberOrUser, nation: models.Nation
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.nation_not_in_alliance(nation),
        color=consts.ERROR_EMBED_COLOR,
    )


def nation(user: MemberOrUser, nation: models.Nation) -> quarrel.Embed:
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
                value=f"{nation.score:,.2f}",
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
                value=f"{nation.average_infrastructure:,.2f}",
            ),
            utils.embed_field(
                name="Average Land",
                value=f"{nation.average_land:,.2f}",
            ),
        ],
    )


def alliance(user: MemberOrUser, alliance: models.Alliance) -> quarrel.Embed:
    members = alliance.members
    member_ids = {i.id for i in members}
    cities = {i for i in cache.cities if i.nation_id in member_ids}
    return utils.build_single_embed_from_user(
        author=user,
        color=consts.INFO_EMBED_COLOR,
        footer_text=strings.model_created("Alliance"),
        timestamp=alliance.date,
        fields=[
            utils.embed_field(
                name="Alliance ID", value=strings.alliance_link(alliance, alliance.id)
            ),
            utils.embed_field(
                name="Name", value=strings.alliance_link(alliance, alliance.name)
            ),
            utils.embed_field(
                name="Acronym", value=strings.alliance_link(alliance, alliance.acronym)
            ),
            utils.embed_field(name="Color", value=strings.enum_name(alliance.color)),
            utils.embed_field(name="Rank", value=f"#{alliance.rank}"),
            utils.embed_field(
                name="Score",
                value=f"{alliance.score:,.2f}",
            ),
            utils.embed_field(
                name="Leaders",
                value="\n".join(
                    strings.nation_link(i, str(i)) for i in alliance.leaders
                ),
            ),
            utils.embed_field(
                name="Members",
                value=f"{len(members):,}",
            ),
            utils.embed_field(
                name="Applicants",
                value=f"{len(alliance.applicants):,}",
            ),
            utils.embed_field(
                name="Forum Link",
                value=strings.click_here_link_or_none(alliance.forum_link),
            ),
            utils.embed_field(
                name="Discord Link",
                value=strings.click_here_link_or_none(alliance.discord_link),
            ),
            utils.embed_field(
                name="Wiki Link",
                value=strings.click_here_link_or_none(alliance.wiki_link),
            ),
            utils.embed_field(
                name="Accepts Members",
                value=alliance.accepts_members,
            ),
            utils.embed_field(
                name="Vacation Mode",
                value=len([i for i in members if i.vacation_mode_turns]),
            ),
            utils.embed_field(
                name="Treasures",
                value=f"{len(alliance.treasures):,}",
            ),
            utils.embed_field(
                name="Average Cities",
                value=f"{sum(i.num_cities for i in members)/len(members):,.2f}",
            ),
            utils.embed_field(
                name="Average Infrastructure",
                value=f"{sum((i.infrastructure for i in cities), start=decimal.Decimal())/len(cities):,.2f}",
            ),
            utils.embed_field(
                name="Average Score",
                value=f"{sum((i.score for i in members), start=decimal.Decimal())/len(members):,.2f}",
            ),
        ],
    )
