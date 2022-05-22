from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import attrs
import lang

from .. import cache, embeds, errors, utils

__all__ = ("Condition",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    import quarrel
    from quarrel import Missing

    from ..commands.common import CommonSlashCommand
    from ..types.quarrel import MemberOrUser


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Condition:
    TABLE: ClassVar[str] = "conditions"
    IGNORE: ClassVar[tuple[str, ...]] = (
        "expression",
        "expression_value",
        "use_condition_expression",
        "use_condition_expression_value",
    )
    id: int
    name: str
    owner_id: int
    value: str
    expression: Optional[lang.Expression] = attrs.field(default=None)
    expression_value: str = attrs.field(default="")
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
    async def convert(
        cls, command: CommonSlashCommand[Any], value: str, parse: bool = False
    ) -> Condition:
        with contextlib.suppress(ValueError):
            condition = cache.get_condition(utils.convert_int(value))
            if condition is not None:
                return condition
        if not parse:
            raise errors.ConditionNotFoundError(command.interaction, value)
        return await Condition.create(
            "",
            command.interaction.user.id,
            lang.parse_expression(value),
            False,
            lang.parse_expression("true"),
        )

    @classmethod
    async def create(
        cls,
        name: str,
        owner_id: int,
        condition: lang.Expression,
        public: bool,
        use_condition: lang.Expression,
    ) -> Condition:
        self = cls(
            id=0,
            name=name,
            owner_id=owner_id,
            value=str(condition),
            public=public,
            use_condition=str(use_condition),
        )
        await self.save()
        cache.add_condition(self)
        return self

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.condition(interaction, self)

    def can_use(self, user: MemberOrUser) -> bool:
        return (
            self.public
            or user.id == self.owner_id
            or self.get_use_condition().evaluate({"user": user})
        )

    async def edit(
        self,
        name: Missing[str],
        condition: Missing[lang.Expression],
        public: Missing[bool],
        use_condition: Missing[lang.Expression],
        owner_id: Missing[int] = quarrel.MISSING,
    ) -> None:
        if name is not quarrel.MISSING:
            self.name = name
        if condition is not quarrel.MISSING:
            self.value = str(condition)
        if public is not quarrel.MISSING:
            self.public = public
        if use_condition is not quarrel.MISSING:
            self.use_condition = str(use_condition)
        if owner_id is not quarrel.MISSING:
            self.owner_id = owner_id
        await self.save()

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

    def get_expression(self) -> lang.Expression:
        if self.value != self.expression_value or self.expression is None:
            expression = lang.parse_expression(self.value)
            self.expression = expression
            self.expression_value = self.value
            return expression
        return self.expression
