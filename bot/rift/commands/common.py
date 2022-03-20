from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import quarrel

from .. import embeds, env, errors

__all__ = ("CommonSlashCommand",)

if TYPE_CHECKING:
    from typing import Any

    from quarrel import Missing
    from quarrel.interactions.command import OptionType

    INT = TypeVar("INT", bound=quarrel.Interaction)

OPTS = TypeVar("OPTS")


class CommonCommand:
    interaction: quarrel.Interaction

    # for some reason this with __slots__ causes a TypeError
    # "multiple bases have instance lay-out conflict"
    # __slots__ = ()

    async def on_error(self, error: Exception) -> None:
        if isinstance(error, quarrel.CheckError):
            error = error.error
        if isinstance(error, errors.GuildOnlyError):
            await self.interaction.respond(
                quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                embeds=[embeds.command_is_guild_only_error(self.interaction.user)],
                ephemeral=True,
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
