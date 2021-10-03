from __future__ import annotations

__all__ = (
    "calc_city",
    "calc_city_sum",
    "calc_city_sum_range",
)


def calc_city(city: int) -> float:
    return 50000 * (city - 2) ** 3 + 150000 * (city - 1) + 75000


def calc_city_sum(city: int) -> float:
    return (
        12500 * (city ** 4) - 25000 * (city ** 3) + 87500 * (city ** 2) + 150000 * city
    )


def calc_city_sum_range(start: int, end: int) -> float:
    return calc_city_sum(end) - calc_city_sum(start)
