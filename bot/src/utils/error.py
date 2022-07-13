from __future__ import annotations

from typing import TYPE_CHECKING

import lark
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
    if isinstance(error, errors.RiftError):
        await respond_with_error(interaction, error.build_embed(interaction))
    elif isinstance(error, lark.UnexpectedToken):
        await respond_with_error(
            interaction, embeds.lark_unexpected_token_error(interaction, error)
        )
    else:
        await respond_with_error(interaction, embeds.fatal_error(interaction))
        return True


async def respond_with_error(
    interaction: quarrel.Interaction, embed: quarrel.Embed
) -> None:
    if interaction.responded:
        await interaction.respond_with_message(
            embed=embed,
            ephemeral=True,
        )
    else:
        await interaction.edit_original_response(
            embed=embed,
        )
