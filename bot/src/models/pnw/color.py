from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("Color",)

if TYPE_CHECKING:
    from typing import ClassVar

    from pnwkit.data import Color as PnWKitColor

    from ...types.models.pnw.color import Color as ColorData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Color:
    TABLE: ClassVar[str] = "colors"
    PRIMARY_KEY: ClassVar[str] = "color"
    color: enums.Color = attrs.field(converter=enums.Color)
    bloc_name: str
    turn_bonus: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: ColorData) -> Color:
        ...

    def to_dict(self) -> ColorData:
        ...

    def update(self, data: Color) -> Color:
        ...

    @property
    def key(self) -> int:
        return self.color.value

    @classmethod
    def from_data(cls, data: PnWKitColor) -> Color:
        return cls(
            color=getattr(enums.Color, data.color.upper()).value,
            bloc_name=data.bloc_name,
            turn_bonus=data.turn_bonus,
        )
