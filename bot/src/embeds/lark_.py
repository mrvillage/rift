from __future__ import annotations

from typing import TYPE_CHECKING

from .. import consts, strings, utils

__all__ = ("lark_unexpected_token_error",)

if TYPE_CHECKING:
    import lark
    import quarrel


def lark_unexpected_token_error(
    interaction: quarrel.Interaction, error: lark.UnexpectedToken
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.lark_unexpected_token_error(error),
        color=consts.ERROR_EMBED_COLOR,
    )
