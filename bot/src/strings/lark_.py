from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("lark_unexpected_token_error",)

if TYPE_CHECKING:
    import lark


def lark_unexpected_token_error(error: lark.UnexpectedToken) -> str:
    return f"Error parsing an expression at line {error.line} column {error.column}!"
