# pyright: reportIncompatibleMethodOverride=false

from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

__all__ = ("MockInteraction",)

if TYPE_CHECKING:
    from typing import Any

    from quarrel.state import State
    from quarrel.types.interactions import Interaction


class MockInteraction(quarrel.Interaction):
    def __init__(self, data: Interaction, state: State) -> None:
        super().__init__(data, state)
        self.requests: list[dict[str, Any]] = []
        self.response: dict[str, Any] = {}
        self.followups: list[dict[str, Any]] = []

    def respond(self, type: quarrel.InteractionCallbackType, **kwargs: Any) -> None:
        self.response = {"type": type, **kwargs}
