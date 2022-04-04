from __future__ import annotations

__all__ = ("convert_comma_separated_ints",)


def convert_comma_separated_ints(value: str) -> list[int]:
    return [convert_int(i) for i in value.split(",")]


def convert_int(value: str) -> int:
    return int(value.replace(",", "").strip())
