from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("InterviewAnswer",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InterviewAnswer:
    TABLE: ClassVar[str] = "interview_answers"
    id: int
    question_id: int
    interview_id: int
    answer: str

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InterviewAnswer:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: InterviewAnswer) -> InterviewAnswer:
        ...
