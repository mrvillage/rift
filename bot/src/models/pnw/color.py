from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Color",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.pnw.color import Color as ColorData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Color:
    TABLE: ClassVar[str] = "colors"
    color: enums.Color = attrs.field(converter=enums.Color)
    bloc_name: str
    turn_bonus: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: ColorData) -> Color:
        ...

    @property
    def key(self) -> int:
        return self.color.value
