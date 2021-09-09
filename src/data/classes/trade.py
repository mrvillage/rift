import json
from datetime import datetime
from typing import TYPE_CHECKING

__all__ = ("TradePrices",)

if TYPE_CHECKING:
    from typings import ResourcePriceData, TradeOfferData, TradePriceData


class TradeOffer:
    __slots__ = ("data", "datetime", "nation_id", "amount", "price", "total_value")

    def __init__(self, data: TradeOfferData):
        self.datetime: datetime = datetime.fromisoformat(data["date"])
        self.nation_id: int = int(data["nationid"])
        self.amount: int = int(data["amount"])
        self.price: int = int(data["price"])
        self.total_value: int = int(data["totalvalue"])


class ResourcePrice:
    __slots__ = (
        "data",
        "name",
        "average_price",
        "avg_price",
        "market_index",
        "highest_buy",
        "lowest_sell",
        "trade_margin",
    )

    def __init__(self, data: ResourcePriceData):
        self.name: str = data["resource"]
        self.average_price: int = int(data["avgprice"])
        self.avg_price: int = self.average_price
        self.market_index: int = int(data["marketindex"].replace(",", ""))
        self.highest_buy: TradeOffer = TradeOffer(data["highestbuy"])
        self.lowest_sell: TradeOffer = TradeOffer(data["lowestbuy"])
        self.trade_margin: int = self.lowest_sell.price - self.highest_buy.price


class TradePrices:
    __slots__ = (
        "data",
        "credit",
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
        "food",
        "market_index",
    )

    def __init__(self, data: TradePriceData):
        self.credit: ResourcePrice = ResourcePrice(data["credit"])
        self.coal: ResourcePrice = ResourcePrice(data["coal"])
        self.oil: ResourcePrice = ResourcePrice(data["oil"])
        self.uranium: ResourcePrice = ResourcePrice(data["uranium"])
        self.lead: ResourcePrice = ResourcePrice(data["lead"])
        self.iron: ResourcePrice = ResourcePrice(data["iron"])
        self.bauxite: ResourcePrice = ResourcePrice(data["bauxite"])
        self.gasoline: ResourcePrice = ResourcePrice(data["gasoline"])
        self.munitions: ResourcePrice = ResourcePrice(data["munitions"])
        self.steel: ResourcePrice = ResourcePrice(data["steel"])
        self.aluminum: ResourcePrice = ResourcePrice(data["aluminum"])
        self.food: ResourcePrice = ResourcePrice(data["food"])
        self.market_index: int = self.credit.market_index

    def _update(self, data, /) -> TradeOffer:
        ...
