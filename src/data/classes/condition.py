from __future__ import annotations

from typing import Any, Dict, List

__all__ = ("Condition",)


class Condition:
    def __init__(self, condition: List[Any]) -> None:
        self.condition: List[Any] = condition

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
            if converter is None:
                converter = NATION_TYPES[chain[1]]
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
        except Exception as e:
            raise ValueError(f"Invalid attribute chain {attribute}.")
        return value

    @classmethod
    def validate_and_create(cls, condition: List[Any]) -> Condition:
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
        return Condition(updated_condition)

    @classmethod
    def parse(cls, condition: str) -> Condition:
        from ...funcs import parse_condition_string

        return cls.validate_and_create(parse_condition_string(condition))
