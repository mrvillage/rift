from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("InterviewConfig",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.interview.interview_config import (
        InterviewConfig as InterviewConfigData,
    )


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InterviewConfig:
    TABLE: ClassVar[str] = "interview_configs"
    id: int
    name: str
    guild_id: int

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: InterviewConfigData) -> InterviewConfig:
        ...
