from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Sequence, Union

from ..query import query_alliances, query_treaties

__all__ = ("Treaties", "Treaty")

if TYPE_CHECKING:
    from typings import TreatyData

    from .alliance import Alliance


class Treaties:
    alliance: Alliance
    treaties: Sequence[Treaty]

    __slots__ = ("alliance", "treaties")

    def __init__(self, alliance: Alliance, treaties: Sequence[Treaty]) -> None:
        self.alliance = alliance
        self.treaties = treaties

    @classmethod
    async def fetch(cls, alliance: Alliance) -> Treaties:
        from .alliance import Alliance

        alliances = await query_alliances()
        alliances = {i[0]: Alliance(data=i) for i in alliances}
        treaties = await query_treaties(alliance.id)
        treaties = [i for i in treaties if i[1] is None]
        treaties = [
            Treaty(dict(i), alliances)
            if i[2] == alliance.id
            else Treaty(dict(i), alliances)
            for i in treaties
        ]
        return cls(alliance, treaties)

    def __str__(self) -> str:
        return "\n".join(str(i) for i in self.treaties)

    def __getitem__(self, index: int) -> Treaty:
        return self.treaties[index]

    def _update(self, data, /) -> Treaties:
        ...


class Treaty:
    started: str
    stopped: str
    from_: Alliance
    to_: Alliance
    treaty_type: str

    __slots__ = ("started", "stopped", "from_", "to_", "treaty_type")

    def __init__(self, data: TreatyData, alliances: Mapping[int, Alliance]) -> None:
        self.started = data[0]
        self.stopped = data[1]
        self.from_ = alliances[data[2]]
        self.to_ = alliances[data[3]]
        self.treaty_type = data[4]

    def __str__(self) -> str:
        if self.treaty_type == "Protectorate":
            return f"**{self.treaty_type}:** {self.from_} --> {self.to_}"
        return f"**{self.treaty_type}:** {self.from_} <--> {self.to_}"

    def _update(self, data, /) -> Treaty:
        ...
