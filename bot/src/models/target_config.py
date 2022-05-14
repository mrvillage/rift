from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("TargetConfig",)

if TYPE_CHECKING:
    from typing import Any, Any, ClassVar

    from .. import flags
    from ..commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetConfig:
    TABLE: ClassVar[str] = "target_configs"
    id: int
    owner_id: int
    name: str
    count: flags.TargetFindCounting
    rater: int
    condition: str
    use_condition: str
    attack: bool
    public: bool

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TargetConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: TargetConfig) -> TargetConfig:
        ...

    @classmethod
    async def convert(
        cls, command: CommonSlashCommand[Any], value: str
    ) -> TargetConfig:
        ...
