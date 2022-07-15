from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import lang

__all__ = ("evaluate_in_default_scope", "merge_expressions")

if TYPE_CHECKING:
    from typing import Any


def evaluate_in_default_scope(expression: lang.Expression, **scope: Any) -> Any:
    return expression.evaluate(DEFAULT_SCOPE | scope)


def merge_expressions(*expressions: lang.Expression | str, sep: str) -> lang.Expression:
    return lang.parse_expression(sep.join(f"({i})" for i in expressions))


DEFAULT_SCOPE: dict[str, Any] = {
    "sum": sum,
    "max": max,
    "min": min,
    "len": len,
    "abs": abs,
    "round": round,
    "all": all,
    "any": any,
    "now": lambda: datetime.datetime.now(tz=datetime.timezone.utc),
}
