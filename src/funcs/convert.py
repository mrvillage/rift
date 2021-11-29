from __future__ import annotations

from typing import Union

from ..data.classes import Alliance, Nation
from ..errors import (
    AllianceNotFoundError,
    NationNotFoundError,
    NationOrAllianceNotFoundError,
)
from ..ref import RiftContext

__all__ = ("convert_nation_or_alliance",)


async def convert_nation_or_alliance(
    ctx: RiftContext, search: str
) -> Union[Nation, Alliance]:
    try:
        return await Nation.convert(ctx, search, False)
    except NationNotFoundError:
        try:
            return await Alliance.convert(ctx, search, False)
        except AllianceNotFoundError:
            try:
                return await Nation.convert(ctx, search, True)
            except NationNotFoundError:
                try:
                    return await Alliance.convert(ctx, search, True)
                except AllianceNotFoundError:
                    raise NationOrAllianceNotFoundError(search)
