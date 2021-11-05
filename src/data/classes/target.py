from __future__ import annotations

import datetime
import time
from typing import TYPE_CHECKING, List, Optional, Union

import discord

from ...cache import cache
from ...data.db import execute_query
from ...errors import TargetNotFoundError
from ...funcs.utils import convert_int
from ...ref import RiftContext
from ..query import add_target_reminder, remove_target_reminder

__all__ = (
    "Target",
    "TargetReminder",
)

if TYPE_CHECKING:
    from _typings import Field, TargetData, TargetReminderData

    from .nation import Nation
    from .resources import Resources
    from .war import Attack, War


class Target:
    __slots__ = ("id", "resources", "last_turn_fetched", "resources_off_attack")

    def __init__(self, data: TargetData) -> None:
        from .resources import Resources

        self.id: int = data["id"]
        resources = data["resources"]
        self.resources: Optional[Resources] = (
            Resources.convert_resources(resources) if resources else None
        )
        self.last_turn_fetched: Optional[str] = data["last_turn_fetched"]
        self.resources_off_attack: bool = data.get("resources_off_attack", True)

    @property
    def nation(self) -> Optional[Nation]:
        return cache.get_nation(self.id)

    @classmethod
    async def create(
        cls,
        nation: Nation,
        revenue: Optional[Resources],
        wars: Optional[List[War]],
        attacks: Optional[List[Attack]],
        /,
        loot: bool = False,
    ) -> Target:  # sourcery no-metrics
        from .resources import Resources

        target = cache.get_target(nation.id)
        data: TargetData = {"id": nation.id}  # type: ignore
        if loot:
            if wars is None:
                wars = await nation.fetch_last_wars()
            if attacks is None:
                attacks_ = [await i.fetch_attacks() for i in wars]
                attacks = []
                for i in attacks_:
                    attacks.extend(i)
            dt = datetime.datetime.utcnow()
            if target is not None and target.last_turn_fetched is not None:
                last_turn_fetched = datetime.datetime.fromisoformat(
                    target.last_turn_fetched
                )
            else:
                last_turn_fetched = datetime.datetime.fromisoformat(
                    "0001-01-01 01:01:01"
                )

            last_turn = dt.replace(
                microsecond=0, second=0, minute=0, hour=dt.hour - dt.hour % 2
            )
            if last_turn > last_turn_fetched:
                revenue = revenue or (await nation.calculate_revenue())["net_income"]
                wars = [
                    i
                    for i in wars
                    if i.attacker_id == nation.id or i.defender_id == nation.id
                ]
                war_ids = {i.id for i in wars}
                attacks = [
                    i for i in attacks if i.type == "victory" and i.war_id in war_ids
                ]
                if attacks:
                    attack = max(attacks, key=lambda x: x.date)
                    resources = Resources.convert_resources(attack.loot_info)
                    difference = dt.replace(
                        second=0, minute=0, hour=dt.hour - dt.hour % 2
                    ) - datetime.datetime.fromisoformat(attack.date)
                    difference
                    days = difference.total_seconds() / 86400
                    resources += revenue * days
                    data["resources_off_attack"] = True
                else:
                    resources = revenue * min(
                        14, (dt - datetime.datetime.fromisoformat(nation.founded)).days
                    )
                    data["resources_off_attack"] = False
                resources = resources
                updated = True
            else:
                resources = None
                updated = False
        else:
            last_turn = None
            resources = None
            updated = False
        data["resources"] = resources and str(resources)
        data["last_turn_fetched"] = last_turn and str(last_turn)
        if target is None:
            target = cls(data)
            await target.save()
        if updated:
            target.resources = resources
            target.last_turn_fetched = last_turn and str(last_turn)
            await target.save()
        return target

    def turn_passed(self, dt: datetime.datetime) -> bool:
        if self.last_turn_fetched is not None:
            last_turn_fetched = datetime.datetime.fromisoformat(self.last_turn_fetched)
        else:
            last_turn_fetched = datetime.datetime.fromisoformat("0001-01-01 01:01:01")

        last_turn = dt.replace(
            microsecond=0, second=0, minute=0, hour=dt.hour - dt.hour % 2
        )
        return last_turn > last_turn_fetched

    async def save(self) -> None:
        cache.add_target(self)
        await execute_query(
            "INSERT INTO targets (id, resources, last_turn_fetched) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET resources = $2, last_turn_fetched = $3 WHERE targets.id = $1;",
            self.id,
            str(self.resources),
            self.last_turn_fetched,
        )

    def rate(
        self,
        nation: Nation,
        /,
        *,
        count_cities: bool = False,
        count_loot: bool = False,
        count_infrastructure: bool = False,
        count_military: bool = False,
        count_activity: bool = False,
    ) -> float:  # sourcery no-metrics
        rating = 0
        target = self.nation
        if target is None:
            return rating

        if count_cities:
            rating += (nation.cities / target.cities) * 10
        if count_military:
            if nation.soldiers and target.soldiers:
                r = (
                    (nation.soldiers - target.soldiers)
                    / 15000
                    / ((nation.cities - target.cities) or 1)
                )
                if nation.soldiers < target.soldiers and nation.cities < target.cities:
                    r *= -1
                rating += r
            elif not nation.soldiers and not target.soldiers:
                pass
            elif not nation.soldiers:
                rating -= 10
            else:
                rating += 10
            if nation.tanks and target.tanks:
                r = (
                    (nation.tanks - target.tanks)
                    / 1250
                    / ((nation.cities - target.cities) or 1)
                )
                if nation.tanks < target.tanks and nation.cities < target.cities:
                    r *= -1
                rating += r
            elif not nation.tanks and not target.tanks:
                pass
            elif not nation.tanks:
                rating -= 10
            else:
                rating += 10
            if nation.aircraft and target.aircraft:
                r = (
                    (nation.aircraft - target.aircraft)
                    / 75
                    / ((nation.cities - target.cities) or 1)
                )
                if nation.aircraft < target.aircraft and nation.cities < target.cities:
                    r *= -1
                rating += r
            elif not nation.aircraft and not target.aircraft:
                pass
            elif not nation.aircraft:
                rating -= 10
            else:
                rating += 10
            if nation.ships and target.ships:
                r = (
                    (nation.ships - target.ships)
                    / 15
                    / ((nation.cities - target.cities) or 1)
                )
                if nation.ships < target.ships and nation.cities < target.cities:
                    r *= -1
                rating += r
            elif not nation.ships and not target.ships:
                pass
            elif not nation.ships:
                rating -= 10
            else:
                rating += 10
        if count_infrastructure:
            rating += (target.get_average_infrastructure() / 500) * 5
        if count_loot and self.resources is not None:
            rating += sum(
                value / 1000
                for key, value in self.resources.to_dict().items()
                if key not in {"credit", "money", "food"}
            )
            rating += self.resources.money / 5_000_000
            rating += self.resources.food / 10_000
        if count_activity:
            dt = datetime.datetime.utcnow()
            last_active = datetime.datetime.fromisoformat(target.last_active)
            delta = dt - last_active
            rating += min(delta.days, 10)

        return rating

    @staticmethod
    def field(
        target: Target,
        nation: Nation,
        rating: float,
        /,
        include_resources: bool = False,
        include_infrastructure: bool = False,
    ) -> Field:
        mil = nation.get_militarization()
        res_string = "\nResources: "
        infra_string = (
            f"\nAverage Infrastructure: {nation.get_average_infrastructure():,.2f}"
        )
        return {
            "name": f"{repr(nation)} ({rating:,.2f})",
            "value": f"[Nation Page](https://politicsandwar.com/nation/id={nation.id})\nLast active <t:{int(time.mktime(datetime.datetime.fromisoformat(nation.last_active).timetuple()))}:R>\nCities: {nation.cities:,}\nSoldiers: {nation.soldiers:,} ({mil['soldiers']:,.2%})\nTanks: {nation.tanks:,} ({mil['tanks']:,.2%})\nAircraft: {nation.aircraft:,} ({mil['aircraft']:,.2%}\nShips: {nation.ships:,} ({mil['ships']:,.2%})\nMissiles: {nation.missiles:,}\nNukes: {nation.nukes}{res_string + str(target.resources) if include_resources else ''}{infra_string if include_infrastructure else ''}",
        }


class TargetReminder:
    __slots__ = (
        "id",
        "target_id",
        "owner_id",
        "channel_ids",
        "role_ids",
        "user_ids",
        "direct_message",
    )

    def __init__(self, data: TargetReminderData) -> None:
        self.id: int = data["id"]
        self.target_id: int = data["target_id"]
        self.owner_id: int = data["owner_id"]
        self.channel_ids: List[int] = data["channel_ids"]
        self.role_ids: List[int] = data["role_ids"]
        self.user_ids: List[int] = data["user_ids"]
        self.direct_message: bool = data["direct_message"]

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str, /) -> TargetReminder:
        try:
            return await cls.fetch(convert_int(argument), ctx.author.id)
        except ValueError:
            raise TargetNotFoundError(argument)

    @classmethod
    async def fetch(cls, reminder_id: int, owner_id: int, /) -> TargetReminder:
        reminder = cache.get_target_reminder(reminder_id)
        if reminder is None:
            raise TargetNotFoundError(reminder_id)
        if reminder.owner_id != owner_id:
            raise TargetNotFoundError(reminder_id)
        return reminder

    def _update(self, data: TargetReminderData) -> None:
        self.id: int = data["id"]
        self.target_id: int = data["target_id"]
        self.owner_id: int = data["owner_id"]
        self.channel_ids: List[int] = data["channel_ids"]
        self.role_ids: List[int] = data["role_ids"]
        self.user_ids: List[int] = data["user_ids"]

    def __int__(self) -> int:
        return self.id

    @property
    def mentions(self) -> str:
        return (
            " ".join(f"<@&{i}>" for i in self.role_ids)
            + " "
            + " ".join(f"<@{i}>" for i in self.user_ids)
        )

    @property
    def nation(self) -> Optional[Nation]:
        return cache.get_nation(self.target_id)

    @classmethod
    async def add(
        cls,
        nation: Nation,
        owner: Union[discord.User, discord.Member],
        channels: List[discord.TextChannel],
        roles: List[discord.Role],
        users: List[Union[discord.User, discord.Member]],
        direct_message: bool = False,
        /,
    ) -> TargetReminder:
        data = await add_target_reminder(
            nation.id,
            owner.id,
            [i.id for i in channels],
            [i.id for i in roles],
            [i.id for i in users],
            direct_message,
        )
        added = cls(data)
        cache.add_target_reminder(added)
        return added

    async def remove(self) -> None:
        await remove_target_reminder(self.id)
        cache.remove_target_reminder(self)
