from __future__ import annotations

import decimal
import re
from enum import Enum
from typing import TYPE_CHECKING

import lark

from . import errors

__all__ = ("parse_expression", "parse_script")

if TYPE_CHECKING:
    from typing import Any, Dict, Final, Optional

    Scope = Dict[str, Any]


def get_attribute(obj: Any, name: str, default: Optional[Any] = None) -> Any:
    try:
        return getattr(obj, name)
    except AttributeError:
        try:
            return obj[name]
        except (KeyError, TypeError) as e:
            if default is not None:
                return default
            raise errors.InvalidAttributeError(
                f"{type(obj).__name__} has no attribute {name}"
            ) from e


def evaluate_if_abstract(value: Any, scope: Scope) -> Any:
    return (
        value.evaluate(scope) if getattr(value, "__lang_abstract__", False) else value
    )


def parse_expression(text: str) -> Expression:
    # the tree_class option is not properly implemented with a TypeVar
    return EXPRESSION_PARSER.parse(text, "expr")  # type: ignore


def parse_script(text: str) -> lark.Tree:
    # the tree_class option is not properly implemented with a TypeVar
    return SCRIPT_PARSER.parse(text, "script")  # type: ignore


def to_string_value(value: Any) -> str:
    return f'"{value}"' if isinstance(value, str) else str(value)


class Operator(Enum):
    __lang_abstract__: Final = True

    or_ = "or"
    and_ = "and"
    lt = "<"
    le = "<="
    ge = ">="
    gt = ">"
    eq = "=="
    ne = "!="
    in_ = "in"
    not_in = "not in"
    is_ = "is"
    is_not = "is not"
    add = "+"
    sub = "-"
    mul = "*"
    div = "/"
    mod = "%"
    floor = "//"
    pow = "**"
    not_ = "not"
    neg = "-"

    def evaluate(self, left: Any, right: Any = None) -> Any:  # noqa: C901
        if self is Operator.or_:
            return left or right
        elif self is Operator.and_:
            return left and right
        elif self is Operator.lt:
            return left < right
        elif self is Operator.le:
            return left <= right
        elif self is Operator.ge:
            return left >= right
        elif self is Operator.gt:
            return left > right
        elif self is Operator.eq:
            return left == right
        elif self is Operator.ne:
            return left != right
        elif self is Operator.in_:
            return left in right
        elif self is Operator.not_in:
            return left not in right
        elif self is Operator.is_:
            return left is right
        elif self is Operator.is_not:
            return left is not right
        elif self is Operator.add:
            return left + right
        elif self is Operator.sub:
            return left - right
        elif self is Operator.mul:
            return left * right
        elif self is Operator.div:
            return left / right
        elif self is Operator.mod:
            return left % right
        elif self is Operator.floor:
            return left // right
        elif self is Operator.pow:
            return left**right
        elif self is Operator.not_:
            return not left
        elif self is Operator.neg:
            return -left


class Member:
    __lang_abstract__: Final = True

    def __init__(self, path: str) -> None:
        self.path: list[Any] = [path]

    def get(self) -> Any:
        ...

    def evaluate(self, scope: Scope) -> Any:  # noqa: C901
        obj = scope[self.path[0]]
        for name in self.path[1:]:
            if isinstance(name, str):
                if name not in get_attribute(obj, "__lang_attrs__", set()):
                    raise errors.InvalidAttributeError(
                        f"{type(obj).__name__} has no attribute {name}"
                    )
                obj = get_attribute(obj, name)
            elif isinstance(name, CSV):
                if not callable(obj) or not get_attribute(
                    obj, "__lang_callable__", True
                ):
                    raise errors.NotCallableError(
                        f"{type(obj).__name__} is not callable"
                    )
                obj = obj(*name.evaluate(scope))
            elif isinstance(name, Index):
                if not get_attribute(obj, "__lang_indexable__", True):
                    raise errors.NotCallableError(
                        f"{type(obj).__name__} is not callable"
                    )
                try:
                    obj = obj[name.evaluate(scope)]
                except TypeError as e:
                    raise errors.InvalidAttributeError(
                        f"{type(obj).__name__} is not subscriptable"
                    ) from e
                except IndexError as e:
                    raise errors.InvalidAttributeError(
                        f"{type(obj).__name__} has no index {name.evaluate(scope)}"
                    ) from e
        return obj

    def chain(self, item: Any) -> Member:
        self.path.append(item)
        return self

    def __str__(self) -> str:
        string = ""
        for name in self.path:
            if isinstance(name, str):
                string += f".{name}"
            elif isinstance(name, CSV):
                string += f"({name})"
            elif isinstance(name, Index):
                string += f"[{name}]"
        return string.strip(".")


class Expression:
    __lang_abstract__: Final = True

    def __init__(
        self, left: Any, operator: Operator, right: Any, expr: bool = False
    ) -> None:
        self.left: Any = left
        self.operator: Operator = operator
        self.right: Any = right
        self.expr: bool = expr

    @classmethod
    def new(cls, left: Any, operator: Operator, right: Any) -> Any:
        if not getattr(left, "__lang_abstract__", False) and not getattr(
            right, "__lang_abstract__", False
        ):
            return operator.evaluate(left, right)
        return cls(left, operator, right)

    def evaluate(self, scope: Scope) -> Any:
        left = evaluate_if_abstract(self.left, scope)
        right = evaluate_if_abstract(self.right, scope)
        return self.operator.evaluate(left, right)

    def __str__(self) -> str:
        return f"{to_string_value(self.left)} {self.operator.value} {to_string_value(self.right)}"


class UnaryExpression:
    __lang_abstract__: Final = True

    def __init__(self, operator: Operator, value: Any) -> None:
        self.operator: Operator = operator
        self.value: Any = value

    @classmethod
    def new(cls, operator: Operator, value: Any) -> Any:
        if not getattr(value, "__lang_abstract__", False):
            return operator.evaluate(value)
        return cls(operator, value)

    def evaluate(self, scope: Scope) -> Any:
        return self.operator.evaluate(self.value.evaluate(scope))

    def __str__(self) -> str:
        if self.operator is Operator.neg:
            return f"-{to_string_value(self.value)}"
        return f"{self.operator.value} {to_string_value(self.value)}"


class CSV:
    __lang_abstract__: Final = True

    def __init__(self, values: list[Any]) -> None:
        self.values: list[Any] = values

    def evaluate(self, scope: Scope) -> Any:
        return [evaluate_if_abstract(i, scope) for i in self.values]

    def __str__(self) -> str:
        return ", ".join(map(to_string_value, self.values))


class Index:
    __lang_abstract__: Final = True

    def __init__(self, values: list[Any]) -> None:
        self.values: list[Any] = values

    def evaluate(self, scope: Scope) -> Any:
        values = [evaluate_if_abstract(i, scope) for i in self.values]
        if len(values) == 1:
            return values[0]
        return slice(*values)

    def __str__(self) -> str:
        return ":".join(map(to_string_value, self.values))


class Map:
    __lang_abstract__: Final = True

    def __init__(self, values: list[Any]) -> None:
        self.values: list[Any] = values

    def evaluate(self, scope: Scope) -> Any:
        return {
            evaluate_if_abstract(self.values[i], scope): evaluate_if_abstract(
                self.values[i + 1], scope
            )
            for i in range(0, len(self.values), 2)
        }

    def __str__(self) -> str:
        return ", ".join(
            f"{to_string_value(self.values[i])}: {to_string_value(self.values[i + 1])}"
            for i in range(0, len(self.values), 2)
        )


class Array:
    __lang_abstract__: Final = True

    def __init__(self, csv: CSV) -> None:
        self.csv: CSV = csv

    def evaluate(self, scope: Scope) -> Any:
        return self.csv.evaluate(scope)

    def __str__(self) -> str:
        return f"[{self.csv}]"


class Object:
    __lang_abstract__: Final = True

    def __init__(self, map: Map) -> None:
        self.map: Map = map

    def evaluate(self, scope: Scope) -> Any:
        return self.map.evaluate(scope)

    def __str__(self) -> str:
        return f"{{{self.map}}}"


class Set:
    __lang_abstract__: Final = True

    def __init__(self, csv: CSV) -> None:
        self.csv: CSV = csv

    def evaluate(self, scope: Scope) -> Any:
        return set(self.csv.evaluate(scope))

    def __str__(self) -> str:
        return f"{{{self.csv}}}"


class LangTransformer:
    def expr(self, tree: list[Any]) -> Any:
        return (
            tree[0]
            if len(tree) == 1
            else Expression(tree[0], tree[1], tree[2], expr=True)
        )

    def nested_expr(self, tree: list[Any]) -> Any:
        tree[0].expr = True
        return tree[0]

    # handle operators

    def condition(self, tree: list[Any]) -> Any:
        return tree[0] if len(tree) == 1 else Expression(tree[0], tree[1], tree[2])

    def operator(self, tree: list[Operator]) -> Any:
        return tree[0]

    def operator_lt(self, tree: list[Operator]) -> Any:
        return Operator.lt

    def operator_le(self, tree: list[Operator]) -> Any:
        return Operator.le

    def operator_ge(self, tree: list[Operator]) -> Any:
        return Operator.ge

    def operator_gt(self, tree: list[Operator]) -> Any:
        return Operator.gt

    def operator_eq(self, tree: list[Operator]) -> Any:
        return Operator.eq

    def operator_ne(self, tree: list[Operator]) -> Any:
        return Operator.ne

    def operator_in(self, tree: list[Operator]) -> Any:
        return Operator.in_

    def operator_not_in(self, tree: list[Operator]) -> Any:
        return Operator.not_in

    def operator_is(self, tree: list[Operator]) -> Any:
        return Operator.is_

    def operator_is_not(self, tree: list[Operator]) -> Any:
        return Operator.is_not

    # handle addition

    def addition_expression(self, tree: list[Any]) -> Any:
        if len(tree) == 1:
            return tree[0]
        else:
            return Expression.new(tree[0], tree[1], tree[2])

    def addition(self, tree: list[Any]) -> Any:
        return tree[0]

    def addition_add(self, tree: list[Any]) -> Any:
        return Operator.add

    def addition_sub(self, tree: list[Any]) -> Any:
        return Operator.sub

    # handle multiplication

    def multiplication_expression(self, tree: list[Any]) -> Any:
        return tree[0] if len(tree) == 1 else tree

    def multiplication(self, tree: list[Any]) -> Any:
        return tree[0]

    def multiplication_mul(self, tree: list[Any]) -> Any:
        return Operator.mul

    def multiplication_div(self, tree: list[Any]) -> Any:
        return Operator.div

    def multiplication_mod(self, tree: list[Any]) -> Any:
        return Operator.mod

    def multiplication_floor(self, tree: list[Any]) -> Any:
        return Operator.floor

    def multiplication_pow(self, tree: list[Any]) -> Any:
        return Operator.pow

    # handle unary

    def unary_expression(self, tree: list[Any]) -> Any:
        return tree[0] if len(tree) == 1 else UnaryExpression(tree[0], tree[1])

    def unary(self, tree: list[Any]) -> Any:
        return tree[0]

    def unary_not(self, tree: lark.Token) -> Any:
        return Operator.not_

    def unary_neg(self, tree: lark.Token) -> Any:
        return Operator.neg

    # handle primary_expression

    def primary_expression(self, tree: list[Any]) -> Any:
        return tree[0]

    # handle literals

    def literal(self, tree: list[Any]) -> Any:
        return tree[0]

    def LITERAL_STRING(self, token: lark.Token) -> str:  # noqa: N802
        return token.value.strip("\"'")

    LITERAL_INT = int
    LITERAL_FLOAT = float

    def LITERAL_DECIMAL(self, token: lark.Token) -> decimal.Decimal:  # noqa: N802
        return decimal.Decimal(token.value[1:])

    def LITERAL_BOOl(self, token: lark.Token) -> bool:  # noqa: N802
        return token.value.lower() == "true"

    def LITERAL_NULL(self, tree: lark.Token) -> None:  # noqa: N802
        return None

    def literal_array(self, tree: list[Any]) -> Array:
        return Array(tree[0])

    def literal_object(self, tree: list[Any]) -> Object:
        return Object(tree[0])

    def literal_set(self, tree: list[Any]) -> Set:
        return Set(tree[0])

    # handle reuseables

    def csv(self, tree: list[Any]) -> CSV:
        return CSV(tree)

    def index(self, tree: list[Any]) -> Index:
        if len(tree) > 3:
            raise errors.InvalidSyntaxError("Index can have at most three arguments")
        return Index(tree)

    def map(self, tree: list[Any]) -> Map:
        return Map(tree)

    # handle members

    def NAME(self, token: lark.Token) -> str:  # noqa: N802
        return token.value

    def member(self, tree: list[Any]) -> Any:
        return tree[0]

    def member_name(self, tree: list[Any]) -> Any:
        return Member(tree[0]) if len(tree) == 1 else tree[0].chain(tree[1])

    def member_call(self, tree: list[Any]) -> Any:
        if isinstance(tree[0], Member):
            return tree[0].chain(CSV([])) if len(tree) == 1 else tree[0].chain(tree[1])
        return Member(tree[0])

    def member_index(self, tree: list[Any]) -> Any:
        if isinstance(tree[0], Member):
            return (
                tree[0].chain(Index([])) if len(tree) == 1 else tree[0].chain(tree[1])
            )
        return Member(tree[0])


OPTIONS = {
    "grammar_filename": "lang.lark",
    "rel_to": __file__,
    "parser": "lalr",
    "debug": True,
    "g_regex_flags": re.M,
    "transformer": LangTransformer(),
    "propagate_positions": True,
    "start": "expr",
    "maybe_placeholders": False,
}
# **options is Unknown
EXPRESSION_PARSER = lark.Lark.open(**OPTIONS)  # type: ignore
# **options is Unknown
SCRIPT_PARSER = lark.Lark.open(**OPTIONS)  # type: ignore
