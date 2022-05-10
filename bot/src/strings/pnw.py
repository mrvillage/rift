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
)

if TYPE_CHECKING:
    from typing import Any, Optional

    from .. import models


def nation_link(nation: models.Nation, text: Any) -> str:
    return f"[{text}](https://politicsandwar.com/nation/id={nation.id})"


def nation_linked_to(nation: models.Nation) -> str:
    user = nation.user
    return f"Linked to <@{user.user_id}>." if user else "Not linked."


def color_and_beige_turns(beige_turns: int) -> str:
    return f"Beige ({beige_turns} turns)."


def alliance_link(alliance: models.Alliance, text: Any) -> str:
    return f"[{text}](https://politicsandwar.com/alliance/id={alliance.id})"


def alliance_link_using_name(alliance: Optional[models.Alliance]) -> str:
    return "None" if alliance is None else alliance_link(alliance, alliance.name)


def city_manager_link(nation: models.Nation, text: Any) -> str:
    return f"[{text}](https://politicsandwar.com/?id=62&n={'+'.join(nation.name.split(' '))})"


def vacation_mode(turns: int) -> str:
    return "False" if turns <= 0 else f"True ({turns} turns)"
