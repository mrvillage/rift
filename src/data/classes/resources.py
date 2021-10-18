from __future__ import annotations

from typing import Dict, Union

from ...funcs.utils import check_resource, convert_number
from ...ref import RiftContext

__all__ = ("Resources",)


class Resources:
    credit: Union[float, int]
    money: Union[float, int]
    food: Union[float, int]
    coal: Union[float, int]
    oil: Union[float, int]
    uranium: Union[float, int]
    lead: Union[float, int]
    iron: Union[float, int]
    bauxite: Union[float, int]
    gasoline: Union[float, int]
    munitions: Union[float, int]
    steel: Union[float, int]
    aluminum: Union[float, int]

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
        return ", ".join(
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
        args = [i.strip(" ,.") for i in argument.split(" ")]
        args = [i if i.lower() != "credits" else "credit" for i in args]
        resources_dict = {}
        if len(args) == 1:
            arg = args[0]
            num = convert_number(arg)
            if arg.startswith("$"):
                resources_dict["money"] = num
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
        if args[-1].startswith("$"):
            resources_dict["money"] = convert_number(args[-1])
        return cls(**resources_dict)

    @classmethod
    async def from_dict(cls, resources: Dict[str, Union[float, int]]) -> Resources:
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

    def __eq__(self, other: Resources) -> bool:
        return self.__dict__ == other.__dict__

    def __ne__(self, other: Resources) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value + other.__dict__[key]
                    for key, value in self.__dict__.items()
                }
            )
        return Resources(**{key: value + other for key, value in self.__dict__.items()})

    def __sub__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value - other.__dict__[key]
                    for key, value in self.__dict__.items()
                }
            )
        return Resources(**{key: value - other for key, value in self.__dict__.items()})

    def __mul__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value * other.__dict__[key]
                    for key, value in self.__dict__.items()
                }
            )
        return Resources(**{key: value * other for key, value in self.__dict__.items()})

    def __truediv__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value / other.__dict__[key]
                    for key, value in self.__dict__.items()
                }
            )
        return Resources(**{key: value / other for key, value in self.__dict__.items()})

    def __pow__(self, other: Union[float, int, Resources]) -> Resources:
        if isinstance(other, Resources):
            return Resources(
                **{
                    key: value ** other.__dict__[key]
                    for key, value in self.__dict__.items()
                }
            )
        return Resources(
            **{key: value ** other for key, value in self.__dict__.items()}
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
