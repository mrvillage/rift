from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = (
    "nation_link",
    "nation_linked_to",
    "color_and_beige_turns",
    "alliance_link",
    "alliance_link_using_name",
    "city_manager_link",
    "vacation_mode",
    "nation_not_in_alliance",
    "user_already_linked",
    "nation_already_linked",
    "nation_username_mismatch",
    "linked_to",
)

if TYPE_CHECKING:
    from typing import Any, Optional

    from .. import models
    from ..types.quarrel import MemberOrUser


def nation_link(nation: models.Nation, text: Any) -> str:
    return f"[{text}](https://politicsandwar.com/nation/id={nation.id})"


def nation_linked_to(nation: models.Nation) -> str:
    user = nation.user
    return f"Linked to <@{user.user_id}>." if user else "Not linked."


def color_and_beige_turns(beige_turns: int) -> str:
    return f"Beige ({beige_turns} turns)"


def alliance_link(alliance: models.Alliance, text: Any) -> str:
    return f"[{text}](https://politicsandwar.com/alliance/id={alliance.id})"


def alliance_link_using_name(alliance: Optional[models.Alliance]) -> str:
    return "None" if alliance is None else alliance_link(alliance, alliance.name)


def city_manager_link(nation: models.Nation, text: Any) -> str:
    return f"[{text}](https://politicsandwar.com/?id=62&n={'+'.join(nation.name.split(' '))})"


def vacation_mode(turns: int) -> str:
    return "False" if turns <= 0 else f"True ({turns} turns)"


def nation_not_in_alliance(nation: models.Nation) -> str:
    return f"{nation} is not in an alliance!"


def user_already_linked(user: MemberOrUser) -> str:
    return f"{user.mention} is already linked to a nation!"


def nation_already_linked(nation: models.Nation) -> str:
    return f"{nation} is already linked to a user!"


def nation_username_mismatch(nation: models.Nation, user: MemberOrUser) -> str:
    return f"The Discord username on {nation}'s page doesn't match {user.mention}!\nHead to https://politicsandwar.com/nation/edit/ and scroll to the very bottom where it says \"Discord Username:\" and put `{user.name}` in the space, hit Save Changes and run the command again!"


def linked_to(nation: models.Nation, user: MemberOrUser) -> str:
    return f"{user.mention} is now linked to {nation}!."
