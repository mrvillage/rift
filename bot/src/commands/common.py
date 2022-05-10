from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import quarrel

from .. import embeds, env, errors

__all__ = ("CommonSlashCommand",)

if TYPE_CHECKING:
    from typing import Any, Protocol

    from quarrel import Missing
    from quarrel.interactions.command import OptionType
    from quarrel.types.interactions import Choice

    INT = TypeVar("INT", bound=quarrel.Interaction)

    class RespondAlias(Protocol):
        async def __call__(
            self,
            *,
            content: Missing[str] = quarrel.MISSING,
            embed: Missing[quarrel.Embed] = quarrel.MISSING,
            embeds: Missing[list[quarrel.Embed]] = quarrel.MISSING,
            # allowed_mentions: Missing[AllowedMentions] = MISSING,
            ephemeral: Missing[bool] = quarrel.MISSING,
            # attachments: Missing[Attachment] = MISSING,
            tts: Missing[bool] = quarrel.MISSING,
            grid: Missing[quarrel.Grid] = quarrel.MISSING,
            choices: Missing[list[Choice]] = quarrel.MISSING,
            # modal: Missing[Modal] = MISSING,
        ) -> None:
            ...


OPTS = TypeVar("OPTS")


class CommonCommand:
    name: str
    interaction: quarrel.Interaction

    async def on_error(self, error: Exception) -> None:
        # original = error
        if isinstance(error, quarrel.CheckError):
            error = error.error
        if isinstance(error, quarrel.OptionError):
            error = error.error
            if isinstance(error, quarrel.ConversionError):
                error = error.errors[0]
        if isinstance(error, errors.GuildOnlyError):
            await self.interaction.respond(
                quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                embeds=[embeds.command_is_guild_only_error(self.interaction.user)],
                ephemeral=True,
            )
        elif isinstance(error, errors.NotFoundError):
            await self.interaction.respond(
                quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                embeds=[
                    embeds.not_found_error(
                        self.interaction.user, error.name, error.value, error.infer
                    )
                ],
                ephemeral=True,
            )
        else:
            await quarrel.SlashCommand.on_error(self, error)  # type: ignore
            await self.respond_with_message(
                embed=embeds.fatal_error(self.interaction.user)
            )

    async def respond_with_message(self, *args: Any, **kwargs: Any) -> None:  # type: ignore
        return await self.interaction.respond(
            quarrel.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE, *args, **kwargs
        )

    respond_with_message: RespondAlias


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
