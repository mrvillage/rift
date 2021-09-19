from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Set

from .data.db import execute_read_query

__all__ = ("cache",)

if TYPE_CHECKING:
    from typings import (
        AllianceData,
        CityData,
        ColorData,
        Link,
        NationData,
        TradePriceData,
        TreatyData,
    )

    from .data.classes import (
        Alliance,
        City,
        Color,
        Embassy,
        EmbassyConfig,
        GuildSettings,
        GuildWelcomeSettings,
        Menu,
        MenuItem,
        Nation,
        Target,
        Ticket,
        TicketConfig,
        TradePrices,
        Treaty,
        UserSettings,
    )


class Validate:
    def __init__(self) -> None:
        self.alliances: bool = False
        self.cities: bool = False
        self.colors: bool = False
        self.nations: bool = False
        self.prices: bool = False
        self.treasures: bool = False
        self.treaties: bool = False


class Cache:
    __slots__ = (
        "_alliances",
        "_cities",
        "_colors",
        "_embassies",
        "_embassy_configs",
        "_guild_settings",
        "_guild_welcome_settings",
        "_links",
        "_menu_interfaces",
        "_menu_items",
        "_menus",
        "_nations",
        "_prices",
        "_targets",
        "_ticket_configs",
        "_tickets",
        "_trades",
        "_treasures",
        "_treaties",
        "_user_settings",
        "_war_attacks",
        "_wars",
        "init",
        "validate",
    )

    def __init__(self):
        self._alliances: Dict[int, Alliance] = {}
        self._cities: Dict[int, City] = {}
        self._colors: Dict[str, Color] = {}
        self._embassies: Dict[int, Embassy] = {}
        self._embassy_configs: Dict[int, EmbassyConfig] = {}
        self._guild_settings: Dict[int, GuildSettings] = {}
        self._guild_welcome_settings: Dict[int, GuildWelcomeSettings] = {}
        self._links: List[Link] = list()
        self._menu_interfaces: List[Dict[str, int]] = list()
        self._menu_items: Dict[int, MenuItem] = {}
        self._menus: Dict[int, Menu] = {}
        self._nations: Dict[int, Nation] = {}
        self._prices: TradePrices
        self._targets: Dict[int, Target] = {}
        self._ticket_configs: Dict[int, TicketConfig] = {}
        self._tickets: Dict[int, Ticket] = {}
        self._trades = {}  # NO CLASS YET
        self._treasures = list()  # NO CLASS YET
        self._treaties: List[Treaty] = list()
        self._user_settings: Dict[int, UserSettings] = {}
        self._war_attacks = {}  # NO CLASS YET
        self._wars = {}  # NO CLASS YET
        self.init: bool = False
        self.validate: Validate = Validate()

    async def initialize(self):  # sourcery no-metrics
        from .data.classes import (
            Alliance,
            City,
            Color,
            Embassy,
            EmbassyConfig,
            GuildSettings,
            GuildWelcomeSettings,
            Menu,
            MenuItem,
            Nation,
            Target,
            Ticket,
            TicketConfig,
            TradePrices,
            Treaty,
        )

        queries = [
            "SELECT * FROM alliances;",
            "SELECT * FROM cities;",
            "SELECT * FROM colors ORDER BY datetime DESC LIMIT 1;",
            "SELECT * FROM embassies;",
            "SELECT * FROM embassy_configs;",
            "SELECT * FROM guild_settings;",
            "SELECT * FROM guild_welcome_settings;",
            "SELECT * FROM links;",
            "SELECT * FROM menu_interfaces;",
            "SELECT * FROM menu_items;",
            "SELECT * FROM menus;",
            "SELECT * FROM nations;",
            "SELECT * FROM prices ORDER BY datetime DESC LIMIT 1;",
            "SELECT * FROM targets;",
            "SELECT * FROM ticket_configs;",
            "SELECT * FROM tickets;",
            "SELECT * FROM treaties;",
        ]
        (
            alliances,
            cities,
            colors,
            embassies,
            embassy_configs,
            guild_settings,
            guild_welcome_settings,
            links,
            menu_interfaces,
            menu_items,
            menus,
            nations,
            prices,
            targets,
            ticket_configs,
            tickets,
            treaties,
        ) = tuple(
            await asyncio.gather(*(execute_read_query(query) for query in queries))
        )
        for i in alliances:
            i = Alliance(i)
            self._alliances[i.id] = i
        for i in cities:
            i = City(i)
            self._cities[i.id] = i
        for i in colors[0]["colors"]:  # SPECIAL CASE
            i = Color(i)
            self._colors[i.name] = i
        for i in embassies:
            i = Embassy(i)
            self._embassies[i.embassy_id] = i
        for i in embassy_configs:
            i = EmbassyConfig(i)
            self._embassy_configs[i.config_id] = i
        for i in guild_settings:
            i = GuildSettings(i)
            self._guild_settings[i.guild_id] = i
        for i in guild_welcome_settings:
            i = GuildWelcomeSettings(i)
            self._guild_welcome_settings[i.guild_id] = i
        for i in links:
            self._links.append(dict(i))  # type: ignore
        for i in menu_interfaces:
            self._menu_interfaces.append(dict(i))  # type: ignore
        for i in menu_items:
            i = MenuItem(i)
            self._menu_items[i.item_id] = i
        for i in menus:
            i = Menu(i)
            self._menus[i.menu_id] = i
        for i in nations:
            i = Nation(i)
            self._nations[i.id] = i
        # for some reason is the only JSON type to give string, so did compatible with proper loading fix here
        self._prices = TradePrices(
            {  # type: ignore
                key: json.loads(value)
                if key != "datetime" and isinstance(value, str)
                else value
                for key, value in dict(prices[0]).items()
            }
        )
        for i in targets:
            i = Target(i)
            self._targets[i.id] = i
        for i in ticket_configs:
            i = TicketConfig(i)
            self._ticket_configs[i.config_id] = i
        for i in tickets:
            i = Ticket(i)
            self._tickets[i.ticket_id] = i
        for i in treaties:
            i = Treaty(
                i,
                {
                    i["from_"]: self.get_alliance(i["from_"]),  # type: ignore
                    i["to_"]: self.get_alliance(i["to_"]),  # type: ignore
                },
            )
            self._treaties.append(i)
        self.init = True

    @property
    def alliances(self) -> Set[Alliance]:
        return set(self._alliances.values())

    @property
    def cities(self) -> Set[City]:
        return set(self._cities.values())

    @property
    def colors(self) -> Set[Color]:
        return set(self._colors.values())

    @property
    def embassies(self) -> Set[Embassy]:
        return set(self._embassies.values())

    @property
    def embassy_configs(self) -> Set[EmbassyConfig]:
        return set(self._embassy_configs.values())

    @property
    def guild_settings(self) -> Set[GuildSettings]:
        return set(self._guild_settings.values())

    @property
    def guild_welcome_settings(self) -> Set[GuildWelcomeSettings]:
        return set(self._guild_welcome_settings.values())

    @property
    def links(self) -> List[Link]:
        return self._links

    @property
    def menu_interfaces(self) -> List[Dict[str, int]]:
        return self._menu_interfaces

    @property
    def menu_items(self) -> Set[MenuItem]:
        return set(self._menu_items.values())

    @property
    def menus(self) -> Set[Menu]:
        return set(self._menus.values())

    @property
    def nations(self) -> Set[Nation]:
        return set(self._nations.values())

    @property
    def prices(self) -> TradePrices:
        return self._prices

    @property
    def targets(self) -> Set[Target]:
        return set(self._targets.values())

    @property
    def ticket_configs(self) -> Set[TicketConfig]:
        return set(self._ticket_configs.values())

    @property
    def tickets(self) -> Set[Ticket]:
        return set(self._tickets.values())

    @property
    def trades(self) -> Set[int]:
        return set(self._trades.values())

    @property
    def treasures(self) -> List[int]:
        return self._treasures

    @property
    def treaties(self) -> List[Treaty]:
        return self._treaties

    @property
    def user_settings(self) -> Set[UserSettings]:
        return set(self._user_settings.values())

    @property
    def war_attacks(self) -> Set[int]:
        return set(self._war_attacks.values())

    @property
    def wars(self) -> Set[int]:
        return set(self._wars.values())

    def hook_alliance(
        self, action: Literal["update", "create", "delete"], data: AllianceData
    ) -> None:
        from .data.classes import Alliance

        if action == "delete":
            del self._alliances[data["id"]]
            return
        try:
            self._alliances[data["id"]]._update(data)
        except KeyError:
            self._alliances[data["id"]] = Alliance(data)

    def hook_city(
        self, action: Literal["update", "create", "delete"], data: CityData
    ) -> None:
        from .data.classes import City

        if action == "delete":
            del self._cities[data["id"]]
            return
        try:
            self._cities[data["id"]]._update(data)
        except KeyError:
            self._cities[data["id"]] = City(data)

    def hook_color(self, action: Literal["update"], data: ColorData) -> None:
        from .data.classes import Color

        try:
            self._colors[data["color"]]._update(data)
        except KeyError:
            self._colors[data["color"]] = Color(data)

    def hook_nation(
        self, action: Literal["update", "create", "delete"], data: NationData
    ) -> None:
        from .data.classes import Nation

        if action == "delete":
            del self._nations[data["id"]]
            return
        try:
            self._nations[data["id"]]._update(data)
        except KeyError:
            self._nations[data["id"]] = Nation(data)

    def hook_price(self, action: Literal["update"], data: TradePriceData) -> None:
        try:
            self._prices._update(data)
        except KeyError:
            self._prices._update(data)

    def hook_treasure(self, action: Literal["update"], data: Dict[Any, Any]) -> None:
        for new in data.values():
            next(i._update(new) for i in self._treasures if i.name == new["name"])

    def hook_treaty(
        self, action: Literal["create", "update", "delete"], data: TreatyData
    ) -> None:
        if action == "update":
            ...  # will need to check if a treaty with those values exists, if it does then update it, if it doesn't then add it
        if action == "delete":
            treaty = next(
                i
                for i in self._treaties
                if i.from_ == data["from_"] and i.to_ == data["to_"]
            )
            return self._treaties.remove(treaty)
        alliances = {
            data["from_"]: self.get_alliance(data["from_"]),
            data["to_"]: self.get_alliance(data["to_"]),
        }
        self._treaties.append(Treaty(list(data.values()), alliances))  # type: ignore

    def get_alliance(self, id: int, /) -> Optional[Alliance]:
        return self._alliances.get(id)

    def get_city(self, id: int, /) -> Optional[City]:
        return self._cities.get(id)

    def get_color(self, name: str, /) -> Optional[Color]:
        return self._colors.get(name)

    def get_embassy(self, id: int, /) -> Optional[Embassy]:
        return self._embassies.get(id)

    def get_embassy_config(self, id: int, /) -> Optional[EmbassyConfig]:
        return self._embassy_configs.get(id)

    def get_guild_settings(self, id: int, /) -> Optional[GuildSettings]:
        return self._guild_settings.get(id)

    def get_guild_welcome_settings(self, id: int, /) -> Optional[GuildWelcomeSettings]:
        return self._guild_welcome_settings.get(id)

    def get_link(self, id: int, /) -> Optional[Link]:
        try:
            return next(
                i for i in self._links if i["user_id"] == id or i["nation_id"] == id
            )
        except StopIteration:
            return

    def get_menu_interface(
        self, menu_id: int, message_id: int, /
    ) -> Optional[Dict[str, int]]:
        try:
            return next(
                i
                for i in self._menu_interfaces
                if i["menu_id"] == menu_id and i["message_id"] == message_id
            )
        except StopIteration:
            return

    def get_menu_item(self, id: int, guild_id: int, /) -> Optional[MenuItem]:
        item = self._menu_items.get(id)
        if item is None:
            return
        if item.guild_id != guild_id:
            return
        return item

    def get_menu(self, id: int, guild_id: int, /) -> Optional[Menu]:
        menu = self._menus.get(id)
        if menu is None:
            return
        if menu.guild_id != guild_id:
            return
        return menu

    def get_nation(self, id: int, /) -> Optional[Nation]:
        return self._nations[id]

    def get_prices(self) -> Optional[TradePrices]:
        return self._prices

    def get_target(self, id: int, owner_id: int, /) -> Optional[Target]:
        target = self._targets.get(id)
        if target is None:
            return
        if target.owner_id != owner_id:
            return
        return target

    def get_ticket_config(self, id: int, /) -> Optional[TicketConfig]:
        return self._ticket_configs.get(id)

    def get_ticket(self, id: int, /) -> Optional[Ticket]:
        return self._tickets.get(id)

    def get_trade(self, id: int, /) -> Optional[int]:
        return self._trades.get(id)

    def get_treasure(self, name: str, /) -> Optional[int]:
        try:
            return next(i for i in self._treasures if i.name == name)
        except StopIteration:
            return

    def get_treaty(self, from_: int, to_: int, treaty_type: str, /) -> Optional[Treaty]:
        try:
            return next(
                i
                for i in self._treaties
                if i.from_ == from_ and i.to_ == to_ and i.treaty_type == treaty_type
            )
        except StopIteration:
            return

    def get_user_settings(self, id: int, /) -> Optional[UserSettings]:
        return self._user_settings.get(id)

    def get_war_attack(self, id: int, /) -> Optional[int]:
        return self._war_attacks.get(id)

    def get_war(self, id: int, /) -> Optional[int]:
        return self._wars.get(id)


cache = Cache()
