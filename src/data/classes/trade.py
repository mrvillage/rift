import json
from datetime import datetime

__all__ = ("TradePrices",)


class TradeOffer:
    __slots__ = ("data", "datetime", "nation_id", "amount", "price", "total_value")

    def __init__(self, data: dict):
        self.data = data
        self.datetime = datetime.fromisoformat(data["date"])
        self.nation_id = int(data["nationid"])
        self.amount = int(data["amount"])
        self.price = int(data["price"])
        self.total_value = int(data["totalvalue"])


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

    def __init__(self, data: dict):
        self.data = data
        self.name = data["resource"]
        self.average_price = int(data["avgprice"])
        self.avg_price = self.average_price
        self.market_index = int(data["marketindex"].replace(",", ""))
        self.highest_buy = TradeOffer(data["highestbuy"])
        self.lowest_sell = TradeOffer(data["lowestbuy"])
        self.trade_margin = self.lowest_sell.price - self.highest_buy.price


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

    def __init__(self, data):
        self.data = data
        self.credit = ResourcePrice(json.loads(data["credit"]))
        self.coal = ResourcePrice(json.loads(data["coal"]))
        self.oil = ResourcePrice(json.loads(data["oil"]))
        self.uranium = ResourcePrice(json.loads(data["uranium"]))
        self.lead = ResourcePrice(json.loads(data["lead"]))
        self.iron = ResourcePrice(json.loads(data["iron"]))
        self.bauxite = ResourcePrice(json.loads(data["bauxite"]))
        self.gasoline = ResourcePrice(json.loads(data["gasoline"]))
        self.munitions = ResourcePrice(json.loads(data["munitions"]))
        self.steel = ResourcePrice(json.loads(data["steel"]))
        self.aluminum = ResourcePrice(json.loads(data["aluminum"]))
        self.food = ResourcePrice(json.loads(data["food"]))
        self.market_index = self.credit.market_index

    def _update(self, data, /) -> TradeOffer:
        ...
