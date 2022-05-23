from __future__ import annotations

from typing import TYPE_CHECKING

import lang

__all__ = ("evaluate_in_default_scope",)

if TYPE_CHECKING:
    from typing import Any


def evaluate_in_default_scope(expression: lang.Expression, **scope: Any) -> Any:
    return expression.evaluate(DEFAULT_SCOPE | scope)


DEFAULT_SCOPE: dict[str, Any] = {
    "sum": sum,
    "max": max,
    "min": min,
    "len": len,
    "abs": abs,
    "round": round,
    "all": all,
    "any": any,
}
