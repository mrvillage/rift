from __future__ import annotations

import re
from typing import TYPE_CHECKING

import lark

__all__ = ("EXPRESSION_PARSER", "parse_expression")

if TYPE_CHECKING:
    from typing import Any


class LangTransformer:
    ...


class Tree(lark.Tree):
    def evaluate(self) -> Any:
        ...


options = {
    "rel_to": __file__,
    "parser": "lalr",
    "debug": True,
    "g_regex_flags": re.M,
    "transformer": LangTransformer(),
    "propagate_positions": True,
    "tree_class": Tree,
    "start": "expr",
    "maybe_placeholders": False,
}
# **options is Unknown
EXPRESSION_PARSER = lark.Lark.open(  # type: ignore
    "lang.lark",
    **options,
)
# **options is Unknown
SCRIPT_PARSER = lark.Lark.open("lang.lark", **options)  # type: ignore


def parse_expression(text: str) -> Tree:
    # the tree_class option is not properly implemented with a TypeVar
    return EXPRESSION_PARSER.parse(text, "expr")  # type: ignore


def parse_script(text: str) -> Tree:
    # the tree_class option is not properly implemented with a TypeVar
    return SCRIPT_PARSER.parse(text, "script")  # type: ignore
