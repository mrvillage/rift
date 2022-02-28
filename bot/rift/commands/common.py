from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import env

__all__ = ("CommonSlashCommand",)

if TYPE_CHECKING:
    from quarrel import Missing
    from quarrel.interactions.command import OptionType, SlashCommand, SlashCommandCheck


class CommonSlashCommand(quarrel.SlashCommand):
    def __init_subclass__(
        cls,
        name: Missing[str] = quarrel.MISSING,
        description: Missing[str] = quarrel.MISSING,
        options: Missing[list[OptionType]] = quarrel.MISSING,
        # pyright has issues unpacking Unions with Type
        parent: type[SlashCommand] = quarrel.MISSING,  # type: ignore
        checks: Missing[list[SlashCommandCheck]] = quarrel.MISSING,
        guilds: Missing[list[int]] = quarrel.MISSING,
        global_: Missing[bool] = quarrel.MISSING,
    ) -> None:
        return super().__init_subclass__(
            name,
            description,
            options,
            # pyright has issues unpacking Unions with Type
            parent,  # type: ignore
            checks,
            guilds or (env.DEV_GUILD_IDS if env.ENVIRONMENT == "dev" else []),
            global_,
        )


class CommonUserCommand(quarrel.UserCommand):
    ...


class CommonMessageCommand(quarrel.MessageCommand):
    ...
