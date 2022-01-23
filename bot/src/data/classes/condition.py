from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, List, Optional, TypeVar, Union

from ...cache import cache
from ...errors import InvalidConditionError
from ...ref import RiftContext
from ..db import execute_query, execute_read_query

__all__ = ("Condition",)

if TYPE_CHECKING:
    from _typings import ConditionData

T = TypeVar("T")


class Condition:
    __slots__ = ("id", "name", "owner_id", "condition", "public")

    def __init__(self, data: ConditionData) -> None:
        self.id: int = data["id"]
        self.name: Optional[str] = data["name"]
        self.owner_id: int = data["owner"]
        self.condition: List[Any] = data["condition"]
        self.public: bool = data["public"]

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE conditions SET name = $2, owner = $3, condition = $4, public = $5 WHERE id = $1;",
                self.id,
                self.name,
                self.owner_id,
                self.condition,
                self.public,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO conditions (name, owner, condition, public) VALUES ($1, $2, $3, $4) RETURNING id;",
                self.name,
                self.owner_id,
                self.condition,
                self.public,
            )
            self.id = id[0]["id"]
            cache.add_condition(self)

    async def remove(self) -> None:
        await execute_query("DELETE FROM conditions WHERE id = $1;", self.id)
        cache.remove_condition(self)

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str):
        try:
            condition = cls.sync_convert(argument, ctx.author.id)
            if condition is None:
                return cls.parse(argument, ctx.author.id)
        except Exception:
            raise InvalidConditionError(argument)
        return condition

    def __repr__(self) -> str:
        return f"c-{self.id}"

    def __str__(self) -> str:
        return self.convert_to_string(self.condition)

    @classmethod
    def convert_to_string(cls, condition: List[Any]) -> str:
        if len(condition) == 1:
            return condition[0]
        return " ".join(cls.convert_to_string(i) if isinstance(i, list) else f"({str(i)[1:-1]})" if isinstance(i, tuple) else str(i) for i in condition)  # type: ignore

    @staticmethod
    def sync_convert(value: str, user_id: int) -> Optional[Condition]:
        from ... import funcs

        if value.startswith(("f-", "c-")):
            value = value[2:]
        try:
            num = funcs.utils.convert_int(value)
            condition = cache.get_condition(num)
            if condition is not None and (
                condition.owner_id == user_id or condition.public
            ):
                return condition
        except ValueError:
            pass
        try:
            return next(
                i
                for i in cache.conditions
                if i.name == value and (i.owner_id == user_id or i.public)
            )
        except StopIteration:
            return

    @staticmethod
    def validate_attribute(attribute: str, value: str) -> Any:  # type: ignore
        from ... import funcs

        chain = attribute.split(".")
        if len(chain) == 1:
            raise ValueError(f"Invalid attribute: {attribute}")

        if chain[0] == "nation":
            converter = funcs.NATION_TYPES[chain[1]]
            if isinstance(converter, dict):
                converter: Any = converter[chain[2]]
        elif chain[0] == "alliance":
            converter = funcs.ALLIANCE_TYPES[chain[1]]
            if isinstance(converter, dict):
                converter: Any = converter[chain[2]]
        else:
            raise ValueError(f"Invalid attribute chain {attribute}.")
        if isinstance(value, tuple):
            val = []
            for i in value:
                try:
                    val.append(converter(i))  # type: ignore
                except Exception:
                    raise ValueError(f"Invalid attribute chain {attribute}.")
            return tuple(val)  # type: ignore
        try:
            value: Any = converter(value)
        except Exception:
            raise ValueError(f"Invalid attribute chain {attribute}.")
        return value

    @classmethod
    def validate_condition(cls, condition: List[Any], user_id: int) -> List[Any]:
        from ...funcs import BOOLEAN_OPERATORS, OPERATORS

        # 1 for attribute, 2 for operator, 3 for value, 4 for boolean operator, 5 for condition
        last = 1
        updated_condition: List[Any] = []
        for index, i in enumerate(condition):
            if last == 2:
                value = cls.validate_attribute(condition[index - 2], i)
                updated_condition.append(value)
                last = 3
            else:
                updated_condition.append(i)
            if i in OPERATORS:
                last = 2
            elif i in BOOLEAN_OPERATORS:
                last = 4
        for index, u in enumerate(updated_condition):
            if isinstance(u, list):
                if len(u) == 1:  # type: ignore
                    if TYPE_CHECKING:
                        assert isinstance(u[0], str)
                    if u[0].startswith(("f", "c")):
                        u[0] = cls.sync_convert(u[0], user_id)
                else:
                    updated_condition[index] = cls.validate_condition(u, user_id)  # type: ignore
        if len(condition) < 3 and not isinstance(condition[0], list):
            raise InvalidConditionError(cls.convert_to_string(condition))
        return updated_condition

    @classmethod
    def validate_and_create(
        cls, condition: List[Any], user_id: int = 0, public: bool = False
    ) -> Condition:
        return cls(
            {
                "id": 0,
                "name": None,
                "owner": user_id,
                "condition": cls.validate_condition(condition, user_id),
                "public": public,
            }
        )

    @classmethod
    def parse(cls, condition: str, user_id: int = 0, public: bool = False) -> Condition:
        from ...funcs import parse_condition_string

        try:
            return cls.validate_and_create(
                parse_condition_string(condition), user_id, public
            )
        except Exception:
            raise InvalidConditionError(condition)

    @staticmethod
    def convert_attribute_value(attributes: List[str], value: Any, /) -> Any:  # type: ignore
        from ... import funcs

        if attributes[0] == "nation":
            converter = funcs.NATION_TYPES[attributes[1]]
            if isinstance(converter, dict):
                converter: Any = converter[attributes[2]]
        elif attributes[0] == "alliance":
            converter = funcs.ALLIANCE_TYPES[attributes[1]]
            if isinstance(converter, dict):
                converter: Any = converter[attributes[2]]
        else:
            return
        return converter(value)

    @classmethod
    def evaluate_expression(
        cls, obj: Any, attribute: str, operator: str, value: Any, /
    ) -> bool:
        attributes = attribute.split(".")
        attr = obj
        for a in attributes[1:]:
            if a in {"id", "rank", "member_count", "score"} and attr is None:
                attr = 0
            elif a in {"name"} and attr is None:
                attr = "None"
            else:
                attr = getattr(attr, a)
        attr = cls.convert_attribute_value(attributes, attr)
        if operator == "==":
            return attr == value
        elif operator == "!=":
            return attr != value
        elif operator == ">>":
            return attr > value
        elif operator == ">=":
            return attr >= value
        elif operator == "<<":
            return attr < value
        elif operator == "<=":
            return attr <= value
        elif operator == "^^":
            return attr in value
        raise SyntaxError(f"Invalid operator {operator}")

    @staticmethod
    def evaluate_boolean_operator(current: bool, operator: str, value: bool, /) -> bool:
        if operator == "&&":
            return current and value
        elif operator == "??":
            return current or value
        elif operator == "!!":
            return not current
        raise SyntaxError(f"Invalid boolean operator {operator}")

    @classmethod
    async def evaluate_condition(cls, obj: Any, condition: List[Any], /) -> bool:
        try:
            if isinstance(condition[0], list):
                current = await cls.evaluate_condition(obj, condition[0])  # type: ignore
                skip = 2
            else:
                current = cls.evaluate_expression(
                    obj, condition[0], condition[1], condition[2]
                )
                skip = 4
            for index, i in enumerate(condition):
                if skip > 0:
                    skip -= 1
                    continue
                if isinstance(i, list):
                    skip = 2
                    value = await cls.evaluate_condition(obj, i)  # type: ignore
                else:
                    skip = 3
                    value = cls.evaluate_expression(obj, condition[index], condition[index + 1], condition[index + 2])  # type: ignore
                current = cls.evaluate_boolean_operator(current, condition[index - 1], value)  # type: ignore
            return current
        except (AttributeError, ValueError):
            raise InvalidConditionError(cls.convert_to_string(condition))

    async def evaluate(self, *values: Any) -> List[bool]:
        evaluated: List[bool] = []
        for index, i in enumerate(values):
            evaluated.append(await self.evaluate_condition(i, self.condition))
            if index % 100:
                await asyncio.sleep(0)
        return evaluated

    async def reduce(self, *values: T) -> List[T]:
        reduced: List[T] = []
        for index, i in enumerate(values):
            if await self.evaluate_condition(i, self.condition):
                reduced.append(i)
            if index % 100:
                await asyncio.sleep(0)
        return reduced

    @classmethod
    def union(cls, *conditions: Union[Condition, List[Any]]) -> Condition:
        conditions_: List[Condition] = []
        for condition in conditions:
            if isinstance(condition, list):
                conditions_.append(cls.validate_and_create(condition))
            elif isinstance(condition, Condition):  # type: ignore
                conditions_.append(condition)
        return Condition.parse("&&".join(str(i) for i in conditions_))