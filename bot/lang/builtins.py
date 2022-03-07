from __future__ import annotations

__all__ = ("augment_builtins",)


def set_lang_attrs(type: tuple[type, ...] | type, *attrs: str) -> None:
    if isinstance(type, tuple):
        for t in type:
            setattr(t, "__lang_attrs__", set(attrs))
    else:
        setattr(type, "__lang_attrs__", set(attrs))


def augment_builtins() -> None:
    set_lang_attrs(
        (bool, int),
        "imag",
        "numerator",
        "real",
        "as_integer_ratio",
        "bit_count",
        "bit_length",
        "conjugate",
        "from_byes",
        "to_byes",
    )
    set_lang_attrs(
        float,
        "imag",
        "real",
        "as_integer_ratio",
        "conjugate",
        "fromhex",
        "hex",
        "is_integer",
    )
    set_lang_attrs(dict, "get")
    set_lang_attrs(list, "index", "count")
    set_lang_attrs(
        set,
        "difference",
        "intersection",
        "isdisjoint",
        "issubset",
        "issuperset",
        "symmetric_difference",
        "union",
    )
    set_lang_attrs(slice, "start", "step", "stop")
    set_lang_attrs(
        str,
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
    )
    set_lang_attrs(tuple, "count", "index")
