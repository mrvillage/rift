from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import lang
import quarrel

from .. import cache, embeds, enums, errors, utils

__all__ = ("Condition",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

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
    def assemble(
        cls,
        name: str,
        owner_id: int,
        condition: lang.Expression,
        use_condition: lang.Expression,
    ) -> Condition:
        return cls(
            id=0,
            name=name,
            owner_id=owner_id,
            value=str(condition),
            use_condition=str(use_condition),
        )

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Condition:
        return utils.convert_model(
            enums.ConvertType.STR_EQ,
            command.interaction,
            value,
            cache.get_condition,
            cache.conditions,
            "name",
            errors.ConditionNotFoundError,
            can_use=True,
        )

    @classmethod
    async def create(
        cls,
        name: str,
        owner_id: int,
        condition: lang.Expression,
        use_condition: lang.Expression,
    ) -> Condition:
        self = cls.assemble(name, owner_id, condition, use_condition)
        await self.save()
        cache.add_condition(self)
        return self

    @classmethod
    def parse(cls, command: CommonSlashCommand[Any], value: str) -> Condition:
        return cls.parse_from_interaction(command.interaction, value)

    @classmethod
    def parse_from_interaction(
        cls, interaction: quarrel.Interaction, value: str
    ) -> Condition:
        return cls.assemble(
            "",
            interaction.user.id,
            lang.parse_expression(value),
            lang.parse_expression("false"),
        )

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.condition(interaction, self)

    def can_use(self, user: MemberOrUser) -> bool:
        return user.id == self.owner_id or utils.evaluate_in_default_scope(
            self.get_use_condition(), user=user
        )

    async def edit(
        self,
        name: Missing[str],
        condition: Missing[lang.Expression],
        use_condition: Missing[lang.Expression],
        owner_id: Missing[int] = quarrel.MISSING,
    ) -> None:
        if name is not quarrel.MISSING:
            self.name = name
        if condition is not quarrel.MISSING:
            self.value = str(condition)
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
