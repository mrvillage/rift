from __future__ import annotations

from typing import Dict, Iterator, Union

from ...funcs.utils import check_resource, convert_number
from ...ref import RiftContext
from .trade import TradePrices

__all__ = ("Resources",)


class Resources:
    __slots__ = (
        "credit",
        "money",
        "food",
        "coal",
        "oil",
        "uranium",
        "lead",
        "iron",
        "bauxite",
        "gasoline",
        "munitions",
        "steel",
        "aluminum",
    )

    def __init__(
        self,
        *,
        credit: Union[float, int] = 0,
        money: Union[float, int] = 0,
        food: Union[float, int] = 0,
        coal: Union[float, int] = 0,
        oil: Union[float, int] = 0,
        uranium: Union[float, int] = 0,
        lead: Union[float, int] = 0,
        iron: Union[float, int] = 0,
        bauxite: Union[float, int] = 0,
        gasoline: Union[float, int] = 0,
        munitions: Union[float, int] = 0,
        steel: Union[float, int] = 0,
        aluminum: Union[float, int] = 0,
    ) -> None:
        self.credit: Union[float, int] = credit
        self.money: Union[float, int] = money
        self.food: Union[float, int] = food
        self.coal: Union[float, int] = coal
        self.oil: Union[float, int] = oil
        self.uranium: Union[float, int] = uranium
        self.lead: Union[float, int] = lead
        self.iron: Union[float, int] = iron
        self.bauxite: Union[float, int] = bauxite
        self.gasoline: Union[float, int] = gasoline
        self.munitions: Union[float, int] = munitions
        self.steel: Union[float, int] = steel
        self.aluminum: Union[float, int] = aluminum

    def __str__(self) -> str:
        resources = [
            i
            for i in (
                ("Credit" if self.credit == 1 else "Credits", self.credit),
                ("Money", self.money),
                ("Food", self.food),
                ("Coal", self.coal),
                ("Oil", self.oil),
                ("Uranium", self.uranium),
                ("Lead", self.lead),
                ("Iron", self.iron),
                ("Bauxite", self.bauxite),
                ("Gasoline", self.gasoline),
                ("Munitions", self.munitions),
                ("Steel", self.steel),
                ("Aluminum", self.aluminum),
            )
            if i[1] != 0
        ]
        return ", ".join(
            f"{value:,.2f} {name}" if name != "Money" else f"${value:,.2f}"
            for name, value in resources
        )

    def to_dict(self) -> Dict[str, Union[float, int]]:
        return {
            "credit": self.credit,
            "money": self.money,
            "food": self.food,
            "coal": self.coal,
            "oil": self.oil,
            "uranium": self.uranium,
            "lead": self.lead,
            "iron": self.iron,
            "bauxite": self.bauxite,
            "gasoline": self.gasoline,
            "munitions": self.munitions,
            "steel": self.steel,
            "aluminum": self.aluminum,
        }

    def newline(self) -> str:
        return "\n".join(
            f"{value:,.2f} {name}"
            for name, value in (
                ("Credit" if self.credit == 1 else "Credits", self.credit),
                ("Money", self.money),
                ("Food", self.food),
                ("Coal", self.coal),
                ("Oil", self.oil),
                ("Uranium", self.uranium),
                ("Lead", self.lead),
                ("Iron", self.iron),
                ("Bauxite", self.bauxite),
                ("Gasoline", self.gasoline),
                ("Munitions", self.munitions),
                ("Steel", self.steel),
                ("Aluminum", self.aluminum),
            )
            if value > 0
        )

    @classmethod
    def convert_resources(cls, argument: str) -> Resources:
        if not argument:
            return cls()
        args = [i.strip(" ,.") for i in argument.split(" ")]
        args = [i if i.lower() != "credits" else "credit" for i in args]
        resources_dict = {}
        if len(args) == 1:
            try:
                arg = args[0]
                num = convert_number(arg)
                if arg.startswith("$"):
                    resources_dict["money"] = num
            except ValueError:
                pass
        for i, arg in enumerate(args[:-1]):
            try:
                num = convert_number(arg)
                if arg.startswith("$"):
                    resources_dict["money"] = num
                elif arg.lower() in ("credit", "credits"):
                    resources_dict["credit"] = num
                elif check_resource(args[i + 1]):
                    resources_dict[args[i + 1].lower()] = num
            except ValueError:
                pass
        try:
            if args[-1].startswith("$"):
                resources_dict["money"] = convert_number(args[-1])
        except ValueError:
            pass
        return cls(**resources_dict)

    @classmethod
    def from_dict(cls, resources: Dict[str, Union[float, int]]) -> Resources:
        return cls(
            money=resources["money"],
            food=resources["food"],
            coal=resources["coal"],
            oil=resources["oil"],
            uranium=resources["uranium"],
            lead=resources["lead"],
            iron=resources["iron"],
            bauxite=resources["bauxite"],
            gasoline=resources["gasoline"],
            munitions=resources["munitions"],
            steel=resources["steel"],
            aluminum=resources["aluminum"],
        )

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Resources:
        return cls.convert_resources(argument)

    def calculate_value(self, prices: TradePrices) -> float:
        return (
            self.money
            + self.food * prices.food.lowest_sell.price
            + self.coal * prices.coal.lowest_sell.price
            + self.oil * prices.oil.lowest_sell.price
            + self.uranium * prices.uranium.lowest_sell.price
            + self.lead * prices.lead.lowest_sell.price
            + self.iron * prices.iron.lowest_sell.price
            + self.bauxite * prices.bauxite.lowest_sell.price
            + self.gasoline * prices.gasoline.lowest_sell.price
            + self.munitions * prices.munitions.lowest_sell.price
            + self.steel * prices.steel.lowest_sell.price
            + self.aluminum * prices.aluminum.lowest_sell.price
        )

    def update(self, other: Resources, /) -> Resources:
        for key, value in other.to_dict().items():
            setattr(self, key, value)
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Resources):
            return self.to_dict() == other.to_dict()
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value + getattr(other, key)
                    for key, value in self.to_dict().items()
                }
            )
        return Resources(
            **{key: value + other for key, value in self.to_dict().items()}
        )

    def __sub__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value - getattr(other, key)
                    for key, value in self.to_dict().items()
                }
            )
        return Resources(
            **{key: value - other for key, value in self.to_dict().items()}
        )

    def __mul__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value * getattr(other, key)
                    for key, value in self.to_dict().items()
                }
            )
        return Resources(
            **{key: value * other for key, value in self.to_dict().items()}
        )

    def __truediv__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value / getattr(other, key)
                    for key, value in self.to_dict().items()
                }
            )
        return Resources(
            **{key: value / other for key, value in self.to_dict().items()}
        )

    def __pow__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value ** getattr(other, key)
                    for key, value in self.to_dict().items()
                }
            )
        return Resources(
            **{key: value**other for key, value in self.to_dict().items()}
        )

    def __iadd__(self, other: Union[float, int]) -> Resources:
        return self.__add__(other)

    def __isub__(self, other: Union[float, int]) -> Resources:
        return self.__sub__(other)

    def __imul__(self, other: Union[float, int]) -> Resources:
        return self.__mul__(other)

    def __itruediv__(self, other: Union[float, int]) -> Resources:
        return self.__truediv__(other)

    def __ipow__(self, other: Union[float, int]) -> Resources:
        return self.__pow__(other)

    def __getitem__(self, item: str) -> float:
        return self.__getattribute__(item)

    def __len__(self) -> int:
        return len([i for i in self.to_dict().values() if i != 0])

    def __iter__(self) -> Iterator[float]:
        return iter([i for i in self.to_dict().values() if i != 0])

    def __lt__(self, other: Union[float, int, Resources]) -> bool:
        if isinstance(other, Resources):
            return any(self[key] < other[key] for key in self.to_dict().keys())
        return any(self[key] < other for key in self.to_dict().keys())

    def __le__(self, other: Union[float, int, Resources]) -> bool:
        if isinstance(other, Resources):
            return all(self[key] <= other[key] for key in self.to_dict().keys())
        return all(self[key] <= other for key in self.to_dict().keys())

    def __gt__(self, other: Union[float, int, Resources]) -> bool:
        if isinstance(other, Resources):
            return any(self[key] > other[key] for key in self.to_dict().keys())
        return any(self[key] > other for key in self.to_dict().keys())

    def __ge__(self, other: Union[float, int, Resources]) -> bool:
        if isinstance(other, Resources):
            return all(self[key] >= other[key] for key in self.to_dict().keys())
        return all(self[key] >= other for key in self.to_dict().keys())
