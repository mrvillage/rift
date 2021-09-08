import json
from datetime import datetime

__all__ = ("TradePrices",)


class TradeOffer:
    __slots__ = ("data", "datetime", "nation_id", "amount", "price", "total_value")

    def __init__(self, data: dict):
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
        self.credit = ResourcePrice(data["credit"])
        self.coal = ResourcePrice(data["coal"])
        self.oil = ResourcePrice(data["oil"])
        self.uranium = ResourcePrice(data["uranium"])
        self.lead = ResourcePrice(data["lead"])
        self.iron = ResourcePrice(data["iron"])
        self.bauxite = ResourcePrice(data["bauxite"])
        self.gasoline = ResourcePrice(data["gasoline"])
        self.munitions = ResourcePrice(data["munitions"])
        self.steel = ResourcePrice(data["steel"])
        self.aluminum = ResourcePrice(data["aluminum"])
        self.food = ResourcePrice(data["food"])
        self.market_index = self.credit.market_index

    def _update(self, data, /) -> TradeOffer:
        ...
