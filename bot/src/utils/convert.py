from __future__ import annotations

from typing import TYPE_CHECKING

from .. import cache, errors

__all__ = (
    "convert_comma_separated_ints",
    "convert_int",
    "self_nation",
    "self_alliance",
)

if TYPE_CHECKING:
    from typing import Any

    from .. import models
    from ..commands.common import CommonSlashCommand


def convert_comma_separated_ints(value: str) -> list[int]:
    return [convert_int(i) for i in value.split(",")]


def convert_int(value: str) -> int:
    return int(value.replace(",", "").strip())


def self_nation(command: CommonSlashCommand[Any]) -> models.Nation:
    user = cache.get_user(command.interaction.user.id)
    if user is None:
        raise errors.NationNotFoundError(command)
    nation = cache.get_nation(user.nation_id)
    if nation is None:
        raise errors.NationNotFoundError(command)
    return nation


def self_alliance(command: CommonSlashCommand[Any]) -> models.Alliance:
    try:
        nation = self_nation(command)
    except errors.NationNotFoundError as e:
        raise errors.AllianceNotFoundError(command) from e
    alliance = nation.alliance
    if alliance is None:
        raise errors.AllianceNotFoundError(command)
    return alliance
