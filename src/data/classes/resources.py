from __future__ import annotations

from typing import Dict, Union

from discord.ext.commands import Context

from ...funcs.utils import check_resource, convert_number
from .base import Base

__all__ = ("Resources",)


class Resources(Base):
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
        credit=0.0,
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
        self.credit = credit
        self.money = money
        self.food = food
        self.coal = coal
        self.oil = oil
        self.uranium = uranium
        self.lead = lead
        self.iron = iron
        self.bauxite = bauxite
        self.gasoline = gasoline
        self.munitions = munitions
        self.steel = steel
        self.aluminum = aluminum

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
    async def convert_resources(cls, argument: str) -> Resources:
        args = [i.strip(" ,.") for i in argument.split(" ")]
        args = [i if i.lower() != "credits" else "credit" for i in args]
        resources_dict = {}
        if len(args) == 1:
            arg = args[0]
            num = await convert_number(arg)
            if arg.startswith("$"):
                resources_dict["money"] = num
        for i, arg in enumerate(args[:-1]):
            try:
                num = await convert_number(arg)
                if arg.startswith("$"):
                    resources_dict["money"] = num
                elif arg.lower() in ("credit", "credits"):
                    resources_dict["credit"] = num
                elif await check_resource(args[i + 1]):
                    resources_dict[args[i + 1].lower()] = num
            except ValueError:
                pass
        if args[-1].startswith("$"):
            resources_dict["money"] = await convert_number(args[-1])
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
    async def convert(cls, ctx: Context, argument: str) -> Resources:
        return await cls.convert_resources(argument)
