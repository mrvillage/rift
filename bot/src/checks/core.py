from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import errors

__all__ = ("guild_only", "modal_guild_only", "button_guild_only", "grid_owner_only")

if TYPE_CHECKING:
    from typing import Any

    from ..commands.common import CommonSlashCommand
    from ..components.common import CommonGrid

    class OwnerOnlyGrid(CommonGrid):
        owner_id: int


@quarrel.check(after_options=False)
async def guild_only(command: CommonSlashCommand[Any]) -> bool:
    if command.interaction.guild_id is quarrel.MISSING:
        raise errors.GuildOnlyError()
    return True


async def modal_guild_only(
    modal: quarrel.Modal[Any],
    interaction: quarrel.Interaction,
    groups: dict[str, str],
    values: Any,
) -> bool:
    if interaction.guild_id is quarrel.MISSING:
        raise errors.GuildOnlyError()
    return True


async def button_guild_only(
    modal: quarrel.Component,
    interaction: quarrel.Interaction,
    groups: dict[str, str],
) -> bool:
    if interaction.guild_id is quarrel.MISSING:
        raise errors.GuildOnlyError()
    return True


async def grid_owner_only(
    grid: quarrel.Grid,
    component: quarrel.Component,
    interaction: quarrel.Interaction,
    groups: dict[str, str],
    values: tuple[str, ...],
) -> bool:
    if TYPE_CHECKING:
        assert isinstance(grid, OwnerOnlyGrid)
    return interaction.user.id == grid.owner_id
