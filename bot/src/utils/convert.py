from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import quarrel

from .. import cache, enums, errors, models

__all__ = (
    "convert_comma_separated_ints",
    "convert_int",
    "self_nation",
    "self_alliance",
    "nation_or_alliance",
    "convert_model",
)

if TYPE_CHECKING:
    from typing import Any, Callable, Iterable, Optional, TypeVar

    from ..commands.common import CommonSlashCommand

    T = TypeVar("T")


def convert_comma_separated_ints(value: str) -> list[int]:
    return [convert_int(i) for i in value.split(",")]


def convert_int(value: str) -> int:
    return int(value.replace(",", "").strip())


def self_nation(command: CommonSlashCommand[Any]) -> models.Nation:
    user = cache.get_user(command.interaction.user.id)
    if user is None or user.nation_id is None:
        raise errors.NationNotFoundError(command.interaction)
    nation = cache.get_nation(user.nation_id)
    if nation is None:
        raise errors.NationNotFoundError(command.interaction)
    return nation


def self_alliance(command: CommonSlashCommand[Any]) -> models.Alliance:
    try:
        nation = self_nation(command)
    except errors.NationNotFoundError as e:
        raise errors.AllianceNotFoundError(command.interaction) from e
    alliance = nation.alliance
    if alliance is None:
        raise errors.AllianceNotFoundError(command.interaction)
    return alliance


async def nation_or_alliance(
    command: CommonSlashCommand[Any], value: str
) -> models.Nation | models.Alliance:
    with contextlib.suppress(errors.NationNotFoundError):
        return await models.Nation.convert(command, value)
    with contextlib.suppress(errors.AllianceNotFoundError):
        return await models.Alliance.convert(command, value)
    raise errors.NationOrAllianceNotFoundError(command.interaction, value)


def convert_model(
    type: enums.ConvertType,
    interaction: quarrel.Interaction,
    value: str,
    getter: Callable[[int], Optional[T]],
    values: Iterable[T],
    values_to_compare: str | set[str],
    error: type[Exception],
    *,
    can_use: bool = False,
) -> T:  # sourcery skip: move-assign
    if isinstance(values_to_compare, str):
        values_to_compare = {values_to_compare}
    value = value.strip()
    with contextlib.suppress(ValueError):
        got = getter(convert_int(value))
        if got is not None and (not can_use or got.can_use(interaction.user)):  # type: ignore
            return got
    lower_value = value.lower()
    if type.value >= 2 and values is not None:
        if (
            len(
                l := [
                    i
                    for i in values
                    if model_strs_compare(i, lower_value, values_to_compare)
                    and (not can_use or i.can_use(interaction.user))  # type: ignore
                ]
            )
            == 1
        ):
            return l[0]
        # add conversions for startswith and endswith, no "the", and partial using in operator
    if type.value >= 3:
        ...  # fuzzy matching here
    raise error(interaction, value)


def str_remove_the(value: str) -> str:
    return value[3:].strip() if value.startswith("the") else value


def model_strs_compare(
    model: Any,
    lower_value: str,
    values_to_compare: set[str],
) -> bool:
    return any(getattr(model, i, "") == lower_value for i in values_to_compare)
