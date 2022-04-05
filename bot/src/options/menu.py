from __future__ import annotations

import quarrel

from .. import enums, models, utils
from .common import CommonOption

__all__ = (
    "MENU_ITEM",
    "MENU",
    "MENU_ITEM_ATTRIBUTES",
    "MENU_ITEM_ATTRIBUTES_OPTIONAL",
    "MENU_ITEM_ROW",
    "MENU_ITEM_ROW_OPTIONAL",
    "MENU_ITEM_COLUMN",
    "MENU_ITEM_COLUMN_OPTIONAL",
)

MENU_ITEM = CommonOption(
    type=quarrel.ApplicationCommandOptionType.NUMBER,
    name="item",
    description="The menu item to use.",
    converter=models.MenuItem.convert,
    min_value=1,
)
MENU = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="menu",
    description="The menu to use.",
    converter=models.Menu.convert,
)
MENU_ITEM_TYPE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="type",
    description="The type of menu item to use.",
    choices=enums.MenuItemType,
)
MENU_ITEM_STYLE = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="style",
    description="The style of menu item to use.",
    default=utils.default_missing,
    choices=enums.MenuItemStyle,
)
MENU_ITEM_LABEL = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="label",
    description="The label to use on the item.",
    default=utils.default_missing,
)
MENU_ITEM_DISABLED = CommonOption(
    type=quarrel.ApplicationCommandOptionType.BOOLEAN,
    name="disabled",
    description="Whether the menu item is disabled.",
    default=utils.default_missing,
)
MENU_ITEM_URL = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="url",
    description="The URL to redirect the item to.",
    default=utils.default_missing,
)
MENU_ITEM_EMOJI = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="emoji",
    description="The emoji to show on item.",
    default=utils.default_missing,
)
MENU_ITEM_ACTION = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="action",
    description="The action to run when the item is clicked.",
    default=utils.default_missing,
    choices=enums.MenuItemAction,
)
MENU_ITEM_ACTION_OPTIONS = CommonOption(
    type=quarrel.ApplicationCommandOptionType.STRING,
    name="action-options",
    description="The options to pass to the action.",
    default=utils.default_missing,
    converter=lambda command, value: utils.convert_comma_separated_ints(value),
)

MENU_ITEM_ATTRIBUTES = (
    MENU_ITEM_TYPE,
    MENU_ITEM_STYLE,
    MENU_ITEM_LABEL,
    MENU_ITEM_DISABLED,
    MENU_ITEM_URL,
    MENU_ITEM_EMOJI,
    MENU_ITEM_ACTION,
    MENU_ITEM_ACTION_OPTIONS,
)
MENU_ITEM_ATTRIBUTES_OPTIONAL = (
    MENU_ITEM_TYPE(default=utils.default_missing),
    MENU_ITEM_STYLE,
    MENU_ITEM_LABEL,
    MENU_ITEM_DISABLED,
    MENU_ITEM_URL,
    MENU_ITEM_EMOJI,
    MENU_ITEM_ACTION,
    MENU_ITEM_ACTION_OPTIONS,
)

MENU_ITEM_ROW = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="row",
    description="The row to put the item in.",
)
MENU_ITEM_ROW_OPTIONAL = MENU_ITEM_ROW(default=utils.default_missing)
MENU_ITEM_COLUMN = CommonOption(
    type=quarrel.ApplicationCommandOptionType.INTEGER,
    name="column",
    description="The column to put the item in.",
)
MENU_ITEM_COLUMN_OPTIONAL = MENU_ITEM_COLUMN(default=utils.default_missing)
