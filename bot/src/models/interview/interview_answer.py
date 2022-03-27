from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("InterviewAnswer",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.interview.interview_answer import (
        InterviewAnswer as InterviewAnswerData,
    )


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InterviewAnswer:
    TABLE: ClassVar[str] = "interview_answers"
    id: int
    question_id: int
    interview_id: int
    answer: str

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: InterviewAnswerData) -> InterviewAnswer:
        ...

    def to_dict(self) -> InterviewAnswerData:
        ...

    def update(self, data: InterviewAnswer) -> InterviewAnswer:
        ...
