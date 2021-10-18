from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from ... import funcs

if TYPE_CHECKING:
    from ...ref import RiftContext
    from .alliance import Alliance
    from .nation import Nation
    from .resources import Resources


class Transaction:
    __slots__ = (
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
        resources: Optional[Resources] = None,
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
    ):
        if resources is None:
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
        else:
            self.money = resources.money
            self.food = resources.food
            self.coal = resources.coal
            self.oil = resources.oil
            self.uranium = resources.uranium
            self.lead = resources.lead
            self.iron = resources.iron
            self.bauxite = resources.bauxite
            self.gasoline = resources.gasoline
            self.munitions = resources.munitions
            self.steel = resources.steel
            self.aluminum = resources.aluminum

    def get_data_withdraw(self):
        return {
            "withmoney": str(self.money),
            "withfood": str(self.food),
            "withcoal": str(self.coal),
            "withoil": str(self.oil),
            "withuranium": str(self.uranium),
            "withlead": str(self.lead),
            "withiron": str(self.iron),
            "withbauxite": str(self.bauxite),
            "withgasoline": str(self.gasoline),
            "withmunitions": str(self.munitions),
            "withsteel": str(self.steel),
            "withaluminum": str(self.aluminum),
            "withsubmit": "Withdraw",
        }

    # type is with for withdraw, dep for deposit (dep will only work if in the main alliance I guess)
    async def complete(self, *, receiver: Union[Alliance, Nation], action: str):
        if action == "send":
            return await funcs.withdraw(transaction=self, receiver=receiver)

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str):
        from .resources import Resources

        return cls(resources=Resources.convert_resources(argument))

    def __str__(self):
        return ", ".join(
            f"{value:,.2f} {name}"
            for name, value in (
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

    def __len__(self):
        return len(
            [
                i
                for i in (
                    self.money,
                    self.food,
                    self.coal,
                    self.oil,
                    self.uranium,
                    self.lead,
                    self.iron,
                    self.bauxite,
                    self.gasoline,
                    self.munitions,
                    self.steel,
                    self.aluminum,
                )
                if i
            ]
        )
