from __future__ import annotations

from .common import CommonFlags, flag

__all__ = ("TargetFindCounting",)


class TargetFindCounting(CommonFlags):
    @flag
    def cities(self) -> int:
        return 1 << 0

    @flag
    def infrastructure(self) -> int:
        return 1 << 1

    @flag
    def activity(self) -> int:
        return 1 << 2

    @flag
    def soldiers(self) -> int:
        return 1 << 3

    @flag
    def tanks(self) -> int:
        return 1 << 4

    @flag
    def aircraft(self) -> int:
        return 1 << 5

    @flag
    def ships(self) -> int:
        return 1 << 6

    @flag
    def missiles(self) -> int:
        return 1 << 7

    @flag
    def nukes(self) -> int:
        return 1 << 8

    @flag
    def money(self) -> int:
        return 1 << 9

    @flag
    def coal(self) -> int:

        return 1 << 10

    @flag
    def oil(self) -> int:
        return 1 << 11

    @flag
    def uranium(self) -> int:
        return 1 << 12

    @flag
    def iron(self) -> int:
        return 1 << 13

    @flag
    def bauxite(self) -> int:
        return 1 << 14

    @flag
    def lead(self) -> int:
        return 1 << 15

    @flag
    def gasoline(self) -> int:
        return 1 << 16

    @flag
    def munitions(self) -> int:
        return 1 << 17

    @flag
    def steel(self) -> int:
        return 1 << 18

    @flag
    def aluminum(self) -> int:
        return 1 << 19

    @flag
    def food(self) -> int:
        return 1 << 20

    @classmethod
    def from_values(cls, values: tuple[str]) -> TargetFindCounting:
        self = cls()
        for i in values:
            setattr(self, i, True)
        return self
