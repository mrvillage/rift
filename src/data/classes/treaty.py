from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Optional

__all__ = ("Treaty",)

if TYPE_CHECKING:
    from _typings import TreatyData

    from .alliance import Alliance


class Treaty:
    started: str
    stopped: Optional[str]
    from_: Alliance
    to_: Alliance
    treaty_type: str

    __slots__ = (
        "started",
        "stopped",
        "from_id",
        "to_id",
        "from_",
        "to_",
        "treaty_type",
    )

    def __init__(self, data: TreatyData, alliances: Mapping[int, Alliance]) -> None:
        self.started = data["started"]
        self.stopped = data["stopped"]
        self.from_id = data["from_"]
        self.to_id = data["to_"]
        self.from_ = alliances[data["from_"]]
        self.to_ = alliances[data["to_"]]
        self.treaty_type = data["treaty_type"]

    def __str__(self) -> str:
        if self.treaty_type == "Protectorate":
            return f"**{self.treaty_type}:** {self.from_} --> {self.to_}"
        return f"**{self.treaty_type}:** {self.from_} <--> {self.to_}"

    def update(self, data: TreatyData, alliances: Mapping[int, Alliance]) -> None:
        self.started = data["started"]
        self.stopped = data["stopped"]
        self.from_id = data["from_"]
        self.to_id = data["to_"]
        self.from_ = alliances[data["from_"]]
        self.to_ = alliances[data["to_"]]
        self.treaty_type = data["treaty_type"]
