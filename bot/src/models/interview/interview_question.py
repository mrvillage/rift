from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("InterviewQuestion",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InterviewQuestion:
    TABLE: ClassVar[str] = "interview_questions"
    id: int
    name: str
    config_id: int
    question: str
    position: int
    answer_type: enums.InterviewAnswerType = attrs.field(
        converter=enums.InterviewAnswerType
    )
    choices: list[str]
    min_choices: int
    max_choices: int

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InterviewQuestion:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: InterviewQuestion) -> InterviewQuestion:
        ...
