from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("get_builtin_attrs",)

if TYPE_CHECKING:
    from typing import Any


def get_builtin_attrs(obj: Any) -> set[str]:
    if isinstance(obj, (bool, int)):
        return {
            "imag",
            "numerator",
            "real",
            "as_integer_ratio",
            "bit_count",
            "bit_length",
            "conjugate",
            "from_byes",
            "to_byes",
        }
    elif isinstance(obj, float):
        return {
            "imag",
            "real",
            "as_integer_ratio",
            "conjugate",
            "fromhex",
            "hex",
            "is_integer",
        }
    elif isinstance(obj, dict):
        return {"get"}
    elif isinstance(obj, list):
        return {"index", "count"}
    elif isinstance(obj, set):
        return {
            "difference",
            "intersection",
            "isdisjoint",
            "issubset",
            "issuperset",
            "symmetric_difference",
            "union",
        }
    elif isinstance(obj, slice):
        return {"start", "step", "stop"}
    elif isinstance(obj, str):
        return {
            "capitalize",
            "casefold",
            "center",
            "count",
            "encode",
            "endswith",
            "expandtabs",
            "find",
            "format",
            "format_map",
            "index",
            "isalnum",
            "isalpha",
            "isascii",
            "isdecimal",
            "isdigit",
            "isidentifier",
            "islower",
            "isnumeric",
            "isprintable",
            "isspace",
            "istitle",
            "isupper",
            "join",
            "ljust",
            "lower",
            "lstrip",
            "maketrans",
            "partition",
            "replace",
            "rfind",
            "rindex",
            "rjust",
            "rpartition",
            "rsplit",
            "rstrip",
            "split",
            "splitlines",
            "startswith",
            "swapcase",
            "title",
            "translate",
            "upper",
            "zfill",
        }
    elif isinstance(obj, tuple):
        return {"count", "index"}
    else:
        return set()
