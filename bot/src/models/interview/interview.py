from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("Interview",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.interview.interview import Interview as InterviewData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Interview:
    TABLE: ClassVar[str] = "interviews"
    id: int
    config_id: int
    owner_id: int
    ticket_id: int
    require_link: bool

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: InterviewData) -> Interview:
        ...

    def to_dict(self) -> InterviewData:
        ...
