from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Credentials",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Credentials:
    TABLE: ClassVar[str] = "credentials"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("nation_id",)
    nation_id: int
    api_key: str

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Credentials:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Credentials) -> Credentials:
        ...
