from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import cache, models, utils

__all__ = ("TargetConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    import lang
    from quarrel import Missing

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

    async def save(self, insert: bool = False) -> None:
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

    @classmethod
    def find_targets(
        cls,
        count: flags.TargetFindCounting,
        rater: models.TargetRater,
        attack: bool,
        expression: Missing[lang.Expression],
        nation: models.Nation,
    ) -> list[models.Target]:
        if attack:
            return [
                models.Target.rate_target(count, rater, i, nation)
                for i in cache.nations
                if i.can_declare_war_on(nation)
                and expression
                and utils.evaluate_in_default_scope(expression, nation=nation, target=i)
            ]
        else:
            return [
                models.Target.rate_target(count, rater, nation, i)
                for i in cache.nations
                if nation.can_declare_war_on(i)
                and expression
                and utils.evaluate_in_default_scope(expression, nation=nation, target=i)
            ]
