from __future__ import annotations

import inspect
import string
from typing import Any, Dict, List

from . import utils

__all__ = (
    "parse_condition_string",
    "BOOLEAN_OPERATORS",
    "OPERATORS",
    "ALLIANCE_TYPES",
    "NATION_TYPES",
)

BOOLEAN_OPERATORS = ("??", "&&", "!!")
BOOLEAN_OPERATOR_CHARACTERS = ("?", "&")
OPERATORS = ("==", "!=", ">", "<", ">=", "<=", "^^")
OPERATOR_CHARACTERS = ("=", ">", "<", "^")
CHARACTERS = string.ascii_letters + string.digits + "._-"
QUOTES = ("'", '"')
ALLIANCE_TYPES: Dict[str, Any] = {"id": lambda x: utils.convert_int(x) if isinstance(x, str) else x}  # type: ignore
NATION_TYPES: Dict[str, Any] = {
    "id": lambda x: utils.convert_int(x) if isinstance(x, str) else x,  # type: ignore
    "alliance": ALLIANCE_TYPES,
    "alliance_position": lambda x: (utils.convert_int(x) if x.isdigit() else utils.get_alliance_position_id(str.capitalize(utils.escape_quoted_string(x))))  # type: ignore
    if isinstance(x, str)
    else x,
    "name": utils.escape_quoted_string,
    "v_mode": lambda x: (bool(utils.convert_int(x)) if x not in {"True", "False"} else x == "True") if isinstance(x, str) else x,  # type: ignore
}


def get_quoted_string(string: str) -> str:
    if string[0] in QUOTES:
        string = string[: string[1:].index(string[0]) + 2]
    return string


def find_bracket_close(condition: str, list_: List[Any]) -> int:
    open = 0
    for index, i in enumerate(condition):
        if i == "(":
            open += 1
        elif i == ")":
            open -= 1
        if open == 0:
            return index
    raise ValueError


def strip(arg: Any) -> Any:
    if isinstance(arg, str):
        return arg.strip()
    elif isinstance(arg, list):
        return [strip(i) for i in arg]  # type: ignore
    elif isinstance(arg, tuple):
        return tuple(strip(i) for i in arg)  # type: ignore
    else:
        return arg


def parse_condition_string(condition: str) -> Any:  # sourcery no-metrics
    name = ""
    boolean_operator = ""
    operator = ""
    arguments: List[Any] = []
    skip_index = 0
    for index, i in enumerate(condition):
        if index < skip_index:
            continue
        if i in QUOTES:
            try:
                quoted = get_quoted_string(condition[index:])
                name = ""
                arguments.append(quoted)
                skip_index = index + len(quoted)
            except ValueError:
                raise SyntaxError(
                    inspect.cleandoc(
                        f"""
                Invalid condition: {condition}\n
                                   {"".join(" " for _ in range(index))}^
                """
                    )
                )
        elif i in CHARACTERS:
            name += i
        elif i == "!":
            boolean_operator += "!"
            operator += "!"
        elif i in BOOLEAN_OPERATOR_CHARACTERS:
            boolean_operator += i
        elif i in OPERATOR_CHARACTERS:
            operator += i
        elif i == "(":
            try:
                condition_ = parse_condition_string(condition[index + 1 :])
                skip_index = (
                    index + find_bracket_close(condition[index:], condition_) + 1
                )
                arguments.append(condition_)
            except ValueError:
                raise SyntaxError(f"Invalid condition: {condition}")
        elif i == ")":
            break
        elif i == "[":
            try:
                condition_ = tuple(
                    get_quoted_string(j.strip())
                    for j in condition[
                        index + 1 : index + condition[index:].index("]")
                    ].split(",")
                )
                arguments.append(condition_)
                skip_index = index + condition[index:].index("]") + 1
            except ValueError:
                raise SyntaxError(
                    inspect.cleandoc(
                        f"""
                Invalid condition: {condition}\n
                                   {"".join(" " for _ in range(index))}^
                """
                    )
                )
        if len(boolean_operator) == 2:
            if name.startswith(("f-", "c-")):
                arguments.append([name])
                name = ""
            elif name:
                arguments.append(name)
                name = ""
            try:
                if (
                    (arguments[-1][0] in CHARACTERS or arguments[-1][0] in QUOTES)
                    and arguments[-2] in OPERATORS
                    and (arguments[-3][0] in CHARACTERS or arguments[-3][0] in QUOTES)
                ) or isinstance(arguments[-1], list):
                    arguments.append(boolean_operator)
                    operator = ""
                    boolean_operator = ""
            except IndexError:
                raise SyntaxError(f"Invalid condition: {condition}")
        elif len(operator) == 2:
            if name:
                arguments.append(name)
                name = ""
            try:
                if arguments[-1][0] in CHARACTERS:
                    arguments.append(operator)
                    boolean_operator = ""
                    operator = ""
            except IndexError:
                raise SyntaxError(
                    inspect.cleandoc(
                        f"""
                Invalid condition: {condition}\n
                                   {"".join(" " for _ in range(index))}^
                """
                    )
                )
    if name:
        arguments.append(name)
    if (
        arguments[-1][0] in OPERATOR_CHARACTERS
        or arguments[-1][0] in BOOLEAN_OPERATOR_CHARACTERS
        or arguments[-1][0] == "!"
        and not isinstance(arguments[-1], (list, tuple))
    ):
        raise SyntaxError(f"Invalid condition: {condition}")
    return strip(arguments)


def validate_condition(condition: Any) -> None:
    for i in condition:
        if isinstance(i, list):
            validate_condition(i)
        elif isinstance(i, tuple):
            ...
        elif i[0] in CHARACTERS:
            ...
