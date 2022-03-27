from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("ServerSubmission",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.server_submission import (
        ServerSubmission as ServerSubmissionData,
    )


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class ServerSubmission:
    TABLE: ClassVar[str] = "server_submissions"
    id: int
    name: str
    invite: str
    description: str
    tags: list[str]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: ServerSubmissionData) -> ServerSubmission:
        ...

    def to_dict(self) -> ServerSubmissionData:
        ...
