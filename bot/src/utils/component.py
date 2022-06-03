from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import utils

__all__ = ("regex_groups_to_model",)

if TYPE_CHECKING:
    from typing import Callable, Optional, TypeVar

    from quarrel import Missing

    T = TypeVar("T")


def regex_groups_to_model(
    interaction: quarrel.Interaction,
    groups: Missing[dict[str, str]],
    getter: Callable[[int], T],
    error: type[Exception],
) -> Optional[T]:
    if groups is quarrel.MISSING:
        return
    try:
        id = utils.convert_int(groups["id"])
    except ValueError:
        return
    value = getter(id)
    if value is None:
        raise error(interaction, id)
    return value
