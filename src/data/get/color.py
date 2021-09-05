from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from ..query import query_colors, query_nation_color_counts

if TYPE_CHECKING:
    from ..classes import Color

__all__ = ("get_colors", "get_nation_color_counts")


async def get_colors() -> Dict[str, Color]:
    from ..classes import Color

    return {str(i["color"]): Color(i) for i in await query_colors()}


async def get_nation_color_counts() -> Dict[str, int]:
    from ...funcs.utils import get_color

    return {get_color(i["color"]): i["count"] for i in await query_nation_color_counts()}  # type: ignore
