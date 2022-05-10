from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import quarrel

from .. import embeds, env, utils

__all__ = ("CommonSlashCommand",)

if TYPE_CHECKING:
    from typing import Any

    from quarrel import Missing
    from quarrel.interactions.command import OptionType


OPTS = TypeVar("OPTS")


class CommonCommand:
    name: str
    interaction: quarrel.Interaction

    async def on_error(self, error: Exception) -> None:
        if utils.handle_interaction_error(self.interaction, error):
            await quarrel.SlashCommand.on_error(self, error)  # type: ignore
            await self.interaction.respond_with_message(
                embed=embeds.fatal_error(self.interaction.user)
            )


class CommonSlashCommand(CommonCommand, quarrel.SlashCommand[OPTS]):
    __slots__ = ()

    def __init_subclass__(
        cls,
        name: Missing[str] = quarrel.MISSING,
        description: Missing[str] = quarrel.MISSING,
        options: Missing[list[OptionType[Any]]] = quarrel.MISSING,
        # pyright has issues unpacking Unions with Type
        parent: type[quarrel.SlashCommand[Any]] = quarrel.MISSING,  # type: ignore
        checks: Missing[list[Any]] = quarrel.MISSING,
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


class CommonUserCommand(CommonCommand, quarrel.UserCommand):
    __slots__ = ()


class CommonMessageCommand(CommonCommand, quarrel.MessageCommand):
    __slots__ = ()
