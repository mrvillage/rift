from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import lang

from .. import cache, embeds, enums, errors, utils

__all__ = ("Tag",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    import quarrel

    from .. import models
    from ..commands.common import CommonSlashCommand
    from ..types.quarrel import MemberOrUser


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Tag:
    TABLE: ClassVar[str] = "tags"
    id: int
    name: str
    owner_id: int
    text: str
    use_condition: str
    use_condition_expression: Optional[lang.Expression] = attrs.field(default=None)
    use_condition_expression_value: str = attrs.field(default="")

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Tag:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Tag) -> Tag:
        ...

    def build_display_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.tag_display(interaction, self)

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.tag(interaction, self)

    def can_use(self, user: MemberOrUser) -> bool:
        return user.id == self.owner_id or utils.evaluate_in_default_scope(
            self.get_use_condition(), user=user
        )

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Tag:
        return utils.convert_model(
            enums.ConvertType.STR_EQ,
            command.interaction,
            value,
            cache.get_tag,
            cache.tags,
            "name",
            errors.TagNotFoundError,
        )

    @classmethod
    async def create(
        cls,
        name: str,
        owner_id: int,
        text: str,
        use_condition: models.Condition,
    ) -> Tag:
        self = cls(
            id=0,
            name=name,
            owner_id=owner_id,
            text=text,
            use_condition=str(use_condition),
        )
        await self.save(insert=True)
        cache.add_tag(self)
        return self

    async def edit(self, name: str, text: str, use_condition: models.Condition) -> None:
        self.name = name
        self.text = text
        self.use_condition = str(use_condition)
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
