from __future__ import annotations

import enum

__all__ = ("InterviewAnswerType",)


class InterviewAnswerType(enum.Enum):
    SHORT_ANSWER = 0
    LONG_ANSWER = 1
    SELECT = 2
