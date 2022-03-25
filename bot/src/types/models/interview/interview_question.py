from __future__ import annotations

from typing import TypedDict

__all__ = ("InterviewQuestion",)


class InterviewQuestion(TypedDict):
    id: int
    name: str
    config_id: int
    question: str
    position: int
    answer_type: int
    choices: list[str]
    min_choices: int
    max_choices: int
