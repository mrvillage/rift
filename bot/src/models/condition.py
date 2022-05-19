from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import embeds, utils

__all__ = ("Condition",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    import lang
    import quarrel

    from ..commands.common import CommonSlashCommand
    from ..types.quarrel import MemberOrUser


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Condition:
    TABLE: ClassVar[str] = "conditions"
    IGNORE: ClassVar[tuple[str, ...]] = (
        "use_condition_expression",
        "use_condition_expression_value",
    )
    id: int
    name: str
    owner_id: int
    value: str
    public: bool
    use_condition: str
    use_condition_expression: Optional[lang.Expression] = attrs.field(default=None)
    use_condition_expression_value: str = attrs.field(default="")

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Condition:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Condition) -> Condition:
        ...

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Condition:
        ...

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.condition(interaction, self)

    def can_use(self, user: MemberOrUser) -> bool:
        return (
            self.public
            or user.id == self.owner_id
            or self.get_use_condition().evaluate({"user": user})
        )

    def get_use_condition(self) -> lang.Expression:
        if (
            self.use_condition != self.use_condition_expression_value
            or self.use_condition_expression is None
        ):
            expression = lang.parse_expression(self.use_condition)
            self.use_condition_expression = expression
            self.use_condition_expression_value = self.use_condition
            return expression
        return self.use_condition_expression
