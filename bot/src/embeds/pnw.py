from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

from .. import strings, utils

__all__ = ("not_found_error",)

if TYPE_CHECKING:
    from typing import Optional


def not_found_error(
    user: quarrel.User | quarrel.Member, name: str, value: Optional[str], infer: bool = False
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=user,
        description=strings.not_found(name, value, infer),
        color=quarrel.Color.RED,
    )
