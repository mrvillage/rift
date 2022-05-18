from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("MenuInterface",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class MenuInterface:
    TABLE: ClassVar[str] = "menu_interfaces"
    id: int
    menu_id: int
    message_id: int
    channel_id: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MenuInterface:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: MenuInterface) -> MenuInterface:
        ...

    # TODO: Add edit message support and update interface support
    async def update_interface(self) -> None:
        ...
