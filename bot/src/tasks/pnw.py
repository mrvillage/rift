from __future__ import annotations

import asyncio
import datetime
from typing import TYPE_CHECKING

import attrs
import pnwkit

from .. import cache, models, utils
from ..bot import bot
from ..env import kit
from .common import CommonTask

__all__ = ("PnWDataTask", "PnWSubscriptionsTask")

if TYPE_CHECKING:
    from typing import Any, Callable

    import pnwkit
    from pnwkit.new import SubscriptionEventLiteral, SubscriptionModelLiteral


async def subscription(
    event: SubscriptionEventLiteral,
    name: str,
    model: SubscriptionModelLiteral,
    cls: Any,
    adder: Callable[[Any], Any],
    getter: Callable[[int], Any],
    remover: Callable[[Any], Any],
) -> None:
    try:
        if event == "create":
            async for i in await kit.subscribe(model, "create"):
                new = cls.from_data(i)
                adder(new)
                await new.save(insert=True)
                bot.dispatch(f"{name}_create", new)
        elif event == "update":
            async for i in await kit.subscribe(model, "update"):
                new = getter(i.id)
                if new is not None:
                    old = attrs.evolve(new)
                    new.update(cls.from_data(i))
                    await new.save()
                    bot.dispatch(f"{name}_update", old, new)
        else:
            async for i in await kit.subscribe(model, "delete"):
                old = cls.from_data(i)
                if old is not None:
                    remover(old)
                    await old.delete()
                    bot.dispatch(f"{name}_delete", old)
    except Exception as e:
        raise e


async def model_subscriptions(
    name: str,
    model: SubscriptionModelLiteral,
    cls: Any,
    adder: Callable[[Any], Any],
    getter: Callable[[int], Any],
    remover: Callable[[Any], Any],
) -> None:
    await asyncio.sleep(1)
    asyncio.create_task(
        subscription("create", name, model, cls, adder, getter, remover),
        name=f"subscribe_{model}_create",
    )
    await asyncio.sleep(1)
    asyncio.create_task(
        subscription("update", name, model, cls, adder, getter, remover),
        name=f"subscribe_{model}_update",
    )
    await asyncio.sleep(1)
    asyncio.create_task(
        subscription("delete", name, model, cls, adder, getter, remover),
        name=f"subscribe_{model}_delete",
    )


class PnWDataTask(CommonTask):
    def __init__(self) -> None:
        super().__init__(interval=60 * 15)
        self.query: pnwkit.Query[pnwkit.Result] = (
            kit.query(
                "treasures", {}, "name color continent bonus spawn_date nation_id"
            )
            .query("colors", {}, "color bloc_name turn_bonus")
            .query("game_info", {}, pnwkit.Field("radiation", {}, ""))
        )

    # ol
    async def before_task(self) -> None:
        next_run = utils.utcnow()
        # set next run equal to the next multiple of four minutes
        next_run = next_run.replace(
            minute=(next_run.minute // 15) * 15, second=0, microsecond=0
        ) + datetime.timedelta(minutes=15)
        # await utils.sleep_until(next_run.timestamp())

    async def task(self) -> None:
        print(
            datetime.datetime.now(datetime.timezone.utc),
            "RUNNING MANUAL PNW DATA TASK",
            flush=True,
        )
        result = await self.query
        treasures = [models.Treasure.from_data(i) for i in result.treasures]
        for i in treasures:
            treasure = cache.get_treasure(i.name)
            if treasure is None:
                cache.add_treasure(i)
                continue
            data = i.to_dict()
            if data != treasure.to_dict():
                old = attrs.evolve(treasure)
                treasure.update(i)
                bot.dispatch("treasure_update", old, treasure)
        colors = [models.Color.from_data(i) for i in result.colors]
        for i in colors:
            color = cache.get_color(i.color)
            if color is None:
                cache.add_color(i)
                continue
            data = i.to_dict()
            if data != color.to_dict():
                old = attrs.evolve(color)
                color.update(i)
                bot.dispatch("color_update", old, color)
        # radiation = models.Radiation.from_data(
        #     result.game_info.radiation, utils.utcnow()
        # )
        print(datetime.datetime.now(datetime.timezone.utc), "done")


class PnWSubscriptionsTask(CommonTask):
    def __init__(self) -> None:
        super().__init__(interval=-1)

    async def task(self) -> None:
        await model_subscriptions(
            "alliance",
            "alliance",
            models.Alliance,
            cache.add_alliance,
            cache.get_alliance,
            cache.remove_alliance,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "bankrec",
            "bankrec",
            models.Bankrec,
            cache.add_bankrec,
            cache.get_bankrec,
            cache.remove_bankrec,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "bounty",
            "bounty",
            models.Bounty,
            cache.add_bounty,
            cache.get_bounty,
            cache.remove_bounty,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "city",
            "city",
            models.City,
            cache.add_city,
            cache.get_city,
            cache.remove_city,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "nation",
            "nation",
            models.Nation,
            cache.add_nation,
            cache.get_nation,
            cache.remove_nation,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "trade",
            "trade",
            models.Trade,
            cache.add_trade,
            cache.get_trade,
            cache.remove_trade,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "treaty",
            "treaty",
            models.Treaty,
            cache.add_treaty,
            cache.get_treaty,
            cache.remove_treaty,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "war_attack",
            "warattack",
            models.WarAttack,
            cache.add_war_attack,
            cache.get_war_attack,
            cache.remove_war_attack,
        )
        await asyncio.sleep(1)
        await model_subscriptions(
            "war",
            "war",
            models.War,
            cache.add_war,
            cache.get_war,
            cache.remove_war,
        )
        # TODO: create models and subscriptions for embargo, treasure_trade, tax_bracket, alliance_position and maybe baseball
