from __future__ import annotations

__all__ = (
    "infrastructure_price",
    "calculate_infrastructure_value",
    "land_price",
    "calculate_land_value",
    "city_price",
    "calculate_city_value",
)


def infrastructure_price(amount: float, /) -> float:
    return ((abs(amount - 10) ** 2.2) / 710) + 300


def calculate_infrastructure_value(start: float, end: float, /) -> float:
    value = 0
    start = round(start, 2)
    end = round(end, 2)
    difference = end - start
    if not difference:
        return 0
    if difference < 0:
        return 150 * difference
    if difference > 100 and difference % 100 == 0:
        chunk = round(infrastructure_price(start), 2) * 100
        return value + chunk + calculate_infrastructure_value(start + 100, end)
    if difference > 100 and difference % 100 != 0:
        chunk = round(infrastructure_price(start), 2) * (difference % 100)
        return (
            value
            + chunk
            + calculate_infrastructure_value(start + difference % 100, end)
        )
    if difference <= 100:
        chunk = round(infrastructure_price(start), 2) * difference
        return value + chunk
    return value


def land_price(amount: float, /) -> float:
    return (0.002 * (amount - 20) * (amount - 20)) + 50


def calculate_land_value(start: float, end: float) -> float:
    value = 0
    start = round(start, 2)
    end = round(end, 2)
    difference = end - start
    if not difference:
        return 0
    if difference < 0:
        return 50 * difference
    if difference > 500 and difference % 500 == 0:
        chunk = round(land_price(start), 2) * 500
        return value + chunk + calculate_land_value(start + 500, end)
    if difference > 500 and difference % 500 != 0:
        chunk = round(land_price(start), 2) * (difference % 500)
        return value + chunk + calculate_land_value(start + difference % 500, end)
    if difference <= 500:
        chunk = round(land_price(start), 2) * difference
        return value + chunk
    return value


def city_price(city: int, /) -> float:
    return 50000 * (city - 2) ** 3 + 150000 * (city - 1) + 75000


def calculate_city_value(start: int, end: int, /) -> float:
    return sum(city_price(i) for i in range(start + 1, end + 1))
