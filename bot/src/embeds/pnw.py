from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import quarrel

from .. import cache, consts, enums, models, strings, utils

__all__ = (
    "not_found_error",
    "nation_not_in_alliance_error",
    "nation",
    "alliance",
    "user_already_linked",
    "nation_already_linked",
    "nation_username_mismatch",
    "linked_to",
)

if TYPE_CHECKING:
    from typing import Optional

    from ..types.quarrel import MemberOrUser


def not_found_error(
    interaction: quarrel.Interaction,
    name: str,
    value: Optional[str],
    infer: bool = False,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.not_found(name, value, infer),
        color=consts.ERROR_EMBED_COLOR,
    )


def nation_not_in_alliance_error(
    interaction: quarrel.Interaction, nation: models.Nation
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.nation_not_in_alliance(nation),
        color=consts.ERROR_EMBED_COLOR,
    )


def nation(interaction: quarrel.Interaction, nation: models.Nation) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        color=consts.INFO_EMBED_COLOR,
        footer_text=strings.model_created_at("Nation"),
        timestamp=nation.date,
        description=strings.nation_linked_to(nation),
        thumbnail_url=nation.flag,
        fields=[
            utils.embed_field("Nation ID", strings.nation_link(nation, nation.id)),
            utils.embed_field("Name", strings.nation_link(nation, nation.name)),
            utils.embed_field("Leader", strings.nation_link(nation, nation.leader)),
            utils.embed_field("War Policy", strings.enum_name(nation.war_policy)),
            utils.embed_field(
                "Domestic Policy",
                strings.enum_name(nation.domestic_policy),
            ),
            utils.embed_field(
                "Continent",
                strings.enum_name(nation.continent),
            ),
            utils.embed_field(
                "Color",
                strings.enum_name(nation.color)
                if nation.color is not enums.Color.BEIGE
                else strings.color_and_beige_turns(nation.beige_turns),
            ),
            utils.embed_field(
                "Alliance", strings.alliance_link_using_name(nation.alliance)
            ),
            utils.embed_field(
                "Alliance Position",
                strings.enum_name(nation.alliance_position),
            ),
            utils.embed_field(
                "Cities",
                strings.city_manager_link(nation, nation.num_cities),
            ),
            utils.embed_field(
                "Score",
                f"{nation.score:,.2f}",
            ),
            utils.embed_field(
                "Vacation Mode",
                strings.vacation_mode(nation.vacation_mode_turns),
            ),
            utils.embed_field(
                "Soldiers",
                f"{nation.soldiers:,}/{nation.num_cities * consts.MAX_SOLDIERS_PER_CITY:,}",
            ),
            utils.embed_field(
                "Tanks",
                f"{nation.tanks:,}/{nation.num_cities * consts.MAX_TANKS_PER_CITY:,}",
            ),
            utils.embed_field(
                "Aircraft",
                f"{nation.aircraft:,}/{nation.num_cities * consts.MAX_AIRCRAFT_PER_CITY:,}",
            ),
            utils.embed_field(
                "Ships",
                f"{nation.ships:,}/{nation.num_cities * consts.MAX_SHIPS_PER_CITY:,}",
            ),
            utils.embed_field(
                "Missiles",
                f"{nation.missiles:,}",
            ),
            utils.embed_field(
                "Nukes",
                f"{nation.nukes:,}",
            ),
            utils.embed_field(
                "Average Infrastructure",
                f"{nation.average_infrastructure:,.2f}",
            ),
            utils.embed_field(
                "Average Land",
                f"{nation.average_land:,.2f}",
            ),
        ],
    )


def alliance(
    interaction: quarrel.Interaction, alliance: models.Alliance
) -> quarrel.Embed:
    members = alliance.members
    member_ids = {i.id for i in members}
    cities = {i for i in cache.cities if i.nation_id in member_ids}
    return utils.build_single_embed_from_user(
        author=interaction.user,
        color=consts.INFO_EMBED_COLOR,
        footer_text=strings.model_created_at("Alliance"),
        timestamp=alliance.date,
        thumbnail_url=alliance.flag,
        fields=[
            utils.embed_field(
                "Alliance ID", strings.alliance_link(alliance, alliance.id)
            ),
            utils.embed_field("Name", strings.alliance_link(alliance, alliance.name)),
            utils.embed_field(
                "Acronym", strings.alliance_link(alliance, alliance.acronym)
            ),
            utils.embed_field("Color", strings.enum_name(alliance.color)),
            utils.embed_field("Rank", f"#{alliance.rank}"),
            utils.embed_field(
                "Score",
                f"{alliance.score:,.2f}",
            ),
            utils.embed_field(
                "Leaders",
                "\n".join(strings.nation_link(i, str(i)) for i in alliance.leaders),
            ),
            utils.embed_field(
                "Members",
                f"{len(members):,}",
            ),
            utils.embed_field(
                "Applicants",
                f"{len(alliance.applicants):,}",
            ),
            utils.embed_field(
                "Forum Link",
                strings.click_here_link_or_none(alliance.forum_link),
            ),
            utils.embed_field(
                "Discord Link",
                strings.click_here_link_or_none(alliance.discord_link),
            ),
            utils.embed_field(
                "Wiki Link",
                strings.click_here_link_or_none(alliance.wiki_link),
            ),
            utils.embed_field(
                "Accepts Members",
                alliance.accepts_members,
            ),
            utils.embed_field(
                "Vacation Mode",
                len([i for i in members if i.vacation_mode_turns]),
            ),
            utils.embed_field(
                "Treasures",
                f"{len(alliance.treasures):,}",
            ),
            utils.embed_field(
                "Average Cities",
                f"{sum(i.num_cities for i in members)/len(members):,.2f}",
            ),
            utils.embed_field(
                "Average Infrastructure",
                f"{sum((i.infrastructure for i in cities), start=decimal.Decimal())/len(cities):,.2f}",
            ),
            utils.embed_field(
                "Average Score",
                f"{sum((i.score for i in members), start=decimal.Decimal())/len(members):,.2f}",
            ),
        ],
    )


def user_already_linked(
    interaction: quarrel.Interaction, user: MemberOrUser
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.user_already_linked(user),
        color=quarrel.Color.RED,
    )


def nation_already_linked(
    interaction: quarrel.Interaction, nation: models.Nation
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.nation_already_linked(nation),
        color=quarrel.Color.RED,
    )


def nation_username_mismatch(
    interaction: quarrel.Interaction,
    nation: models.Nation,
    user: MemberOrUser,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.nation_username_mismatch(nation, user),
        color=quarrel.Color.RED,
    )


def linked_to(
    interaction: quarrel.Interaction, nation: models.Nation, user: MemberOrUser
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.linked_to(nation, user),
        color=quarrel.Color.GREEN,
    )
