def calc_city(city: int):
    return 50000 * (city - 2) ** 3 + 150000 * (city - 1) + 75000


def calc_city_sum(city: int):
    return (
        12500 * (city ** 4) - 25000 * (city ** 3) + 87500 * (city ** 2) + 150000 * city
    )


def calc_city_sum_range(start: int, end: int):
    return calc_city_sum(end) - calc_city_sum(start)
