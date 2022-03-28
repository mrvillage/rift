from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("TargetConfig",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.target_config import TargetConfig as TargetConfigData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetConfig:
    TABLE: ClassVar[str] = "target_configs"
    id: int
    owner_id: int
    name: str
    count: int
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
    def from_dict(cls, data: TargetConfigData) -> TargetConfig:
        ...

    def to_dict(self) -> TargetConfigData:
        ...

    def update(self, data: TargetConfig) -> TargetConfig:
        ...
