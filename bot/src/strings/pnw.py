from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("not_found",)

if TYPE_CHECKING:
    from typing import Optional


def not_found(name: str, value: Optional[str], infer: bool = False) -> str:
    if value is None and infer:
        return f"Your Discord account is not linked to a nation so I couldn't infer your {name}!"
    return f"No {name} found with argument `{value}`."
