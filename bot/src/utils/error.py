from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import embeds, errors

__all__ = ("handle_interaction_error",)

if TYPE_CHECKING:
    from typing import Optional


async def handle_interaction_error(
    interaction: quarrel.Interaction, error: Exception
) -> Optional[bool]:
    if isinstance(error, quarrel.CheckError):
        error = error.error
    if isinstance(error, quarrel.OptionError):
        error = error.error
        if isinstance(error, quarrel.ConversionError):
            error = error.errors[0]
    if isinstance(error, errors.GuildOnlyError):
        await respond_with_error(interaction, embeds.command_is_guild_only_error(interaction.user))
    elif isinstance(error, errors.NotFoundError):
        await respond_with_error(
            interaction,
            embeds.not_found_error(
                interaction.user, error.name, error.value, error.infer
            ),
        )
    else:
        return True


async def respond_with_error(
    interaction: quarrel.Interaction, embed: quarrel.Embed
) -> None:
    await interaction.respond_with_message(
        embed=embed,
        ephemeral=True,
    )
