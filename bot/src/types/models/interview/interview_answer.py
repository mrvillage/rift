from __future__ import annotations

from typing import TypedDict

__all__ = ("InterviewAnswer",)


class InterviewAnswer(TypedDict):
    id: int
    question_id: int
    interview_id: int
    answer: str
