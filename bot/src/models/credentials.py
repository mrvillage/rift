from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Credentials",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.credentials import Credentials as CredentialsData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Credentials:
    TABLE: ClassVar[str] = "credentials"
    PRIMARY_KEY: ClassVar[str] = "nation_id"
    nation_id: int
    api_key: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: CredentialsData) -> Credentials:
        ...

    def to_dict(self) -> CredentialsData:
        ...

    def update(self, data: Credentials) -> Credentials:
        ...
