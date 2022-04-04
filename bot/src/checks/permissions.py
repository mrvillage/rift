from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import errors

__all__ = (
    "has_alliance_role_permissions",
    "has_discord_role_permissions",
    "has_guild_role_permissions",
)

if TYPE_CHECKING:
    from typing import Any, Callable, Coroutine

    from ..commands.common import CommonSlashCommand


async def has_alliance_role_permissions(
    **permissions: bool,
) -> Callable[[CommonSlashCommand[Any]], Coroutine[Any, Any, bool]]:
    @quarrel.check(after_options=True, requires=["alliance"])
    async def check(command: CommonSlashCommand[Any]) -> bool:
        return True

    return check


async def has_discord_role_permissions(
    **permissions: bool,
) -> Callable[[CommonSlashCommand[Any]], Coroutine[Any, Any, bool]]:
    @quarrel.check(after_options=False)
    async def check(command: CommonSlashCommand[Any]) -> bool:
        if command.interaction.guild_id is quarrel.MISSING:
            raise errors.GuildOnlyError()
        if TYPE_CHECKING:
            assert isinstance(command.interaction.user, quarrel.Member)
        perms = command.interaction.user.permissions
        if all(getattr(perms, name) is value for name, value in permissions.items()):
            return True
        raise errors.MissingDiscordPermissionsError(permissions)

    return check


async def has_guild_role_permissions(
    **permissions: bool,
) -> Callable[[CommonSlashCommand[Any]], Coroutine[Any, Any, bool]]:
    @quarrel.check(after_options=False)
    async def check(command: CommonSlashCommand[Any]) -> bool:
        return True

    return check
