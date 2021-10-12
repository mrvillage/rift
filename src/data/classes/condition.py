from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.data.db.sql import execute_query

from ...cache import cache
from ...data.db import execute_read_query

__all__ = ("Condition",)

if TYPE_CHECKING:
    from _typings import ConditionData


class Condition:
    __slots__ = ("id", "name", "owner_id", "condition")

    def __init__(self, data: ConditionData) -> None:
        self.id: int = data.get("id")
        self.name: Optional[str] = data["name"]
        self.owner_id: Optional[int] = data["owner_id"]
        self.condition: List[Any] = data["condition"]

    async def save(self) -> None:
        if self.id is None:
            id = await execute_read_query(
                "INSERT INTO conditions (name, owner_id, condition) VALUES ($1, $2, $3) RETURNING id;",
                self.name,
                self.owner_id,
                self.condition,
            )
            self.id = id[0]["id"]
            cache.add_condition(self)
        else:
            await execute_query(
                "UPDATE conditions SET name = $2, owner_id = $3, condition = $4 WHERE id = $1;",
                self.id,
                self.name,
                self.owner_id,
                self.condition,
            )

    @staticmethod
    def sync_convert(value: str, user_id: int) -> Optional[Condition]:
        from ... import funcs

        if value.startswith(("f-", "c-")):
            value = value.replace("f-", "").replace("c-", "")
        num = funcs.utils.convert_int(value)
        condition = cache.get_condition(num, user_id)
        if condition is not None:
            return condition
        try:
            return next(
                i
                for i in cache.conditions
                if i.name == value and (i.owner_id == user_id or i.owner_id is None)
            )
        except StopIteration:
            return

    @staticmethod
    def validate_attribute(attribute: str, value: str) -> Any:  # type: ignore
        from ... import funcs

        ALLIANCE_TYPES: Dict[str, Any] = {"id": funcs.utils.convert_int}
        NATION_TYPES: Dict[str, Any] = {
            "alliance": ALLIANCE_TYPES,
            "alliance_position": (
                funcs.utils.escape_quoted_string,
                str.capitalize,
                funcs.utils.get_alliance_position_id,
            ),
            "name": funcs.utils.escape_quoted_string,
        }

        chain = attribute.split(".")
        if len(chain) == 1:
            raise ValueError(f"Invalid attribute: {attribute}")

        if chain[0] == "nation":
            converter = NATION_TYPES[chain[1]]
            if isinstance(converter, dict):
                converter: Any = converter[chain[2]]
        elif chain[0] == "alliance":
            converter = ALLIANCE_TYPES[chain[1]]
            if isinstance(converter, dict):
                converter: Any = converter[chain[2]]
        else:
            raise ValueError(f"Invalid attribute chain {attribute}.")
        try:
            if isinstance(converter, tuple):
                for conv in converter:  # type: ignore
                    value: Any = conv(value)
            else:
                value: Any = converter(value)
        except Exception:
            raise ValueError(f"Invalid attribute chain {attribute}.")
        return value

    @classmethod
    def validate_and_create(cls, condition: List[Any], user_id: int, /) -> Condition:
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
        for u in updated_condition:
            if isinstance(u, list) and len(u) == 1:  # type: ignore
                if TYPE_CHECKING:
                    assert isinstance(u[0], str)
                if u[0].startswith(("f", "c")):
                    u[0] = cls.sync_convert(u[0], user_id)
        return Condition(
            {
                "id": None,  # type: ignore
                "name": None,
                "owner_id": user_id,
                "condition": updated_condition,
            }
        )

    @classmethod
    def parse(cls, condition: str, user_id: int, /) -> Condition:
        from ...funcs import parse_condition_string

        return cls.validate_and_create(parse_condition_string(condition), user_id)
