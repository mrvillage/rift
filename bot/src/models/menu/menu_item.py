from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import quarrel

from ... import cache, components, consts, embeds, enums, errors, models, utils

__all__ = ("MenuItem",)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Optional

    from quarrel import Missing
    from typing_extensions import Self

    from ...commands.common import CommonSlashCommand


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class MenuItem:
    TABLE: ClassVar[str] = "menu_items"
    ENUMS: ClassVar[tuple[str, ...]] = ("type", "style", "action")
    id: int
    menu_id: int
    type: enums.MenuItemType = attrs.field(converter=enums.MenuItemType)
    style: enums.MenuItemStyle = attrs.field(converter=enums.MenuItemStyle)
    label: Optional[str]
    disabled: Optional[bool]
    url: Optional[str]
    emoji: Optional[int]
    action: enums.MenuItemAction = attrs.field(converter=enums.MenuItemAction)
    action_options: list[int]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MenuItem:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: MenuItem) -> MenuItem:
        ...

    @property
    def menu(self) -> Optional[models.Menu]:
        return cache.get_menu(self.menu_id)

    @property
    def width(self) -> int:
        if self.type is enums.MenuItemType.BUTTON:
            return consts.BUTTON_WIDTH
        elif self.type is enums.MenuItemType.SELECT_MENU:
            return consts.SELECT_MENU_WIDTH
        return consts.DEFAULT_COMPONENT_WIDTH

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> MenuItem:
        return utils.convert_model(
            enums.ConvertType.ID,
            command.interaction,
            value,
            cache.get_menu_item,
            set(),
            set(),
            errors.MenuItemNotFoundError,
        )

    @classmethod
    async def create(
        cls,
        menu: models.Menu,
        type: enums.MenuItemType,
        style: Missing[enums.MenuItemStyle],
        label: Missing[str],
        disabled: Missing[bool],
        url: Missing[str],
        emoji: Missing[int],
        action: Missing[enums.MenuItemAction],
        action_options: Missing[list[int]],
        row: Missing[int],
        column: Missing[int],
    ) -> Self:
        self = cls(
            id=0,
            menu_id=menu.id,
            type=type,
            style=style or enums.MenuItemStyle.BLURPLE,
            label=label or None,
            disabled=disabled if disabled is not quarrel.MISSING else False,
            url=url or None,
            emoji=emoji or None,
            action=action or enums.MenuItemAction.NONE,
            action_options=action_options or [],
        )
        if not menu.has_space(self.width, row, column):
            raise errors.MenuHasNoSpaceError(menu, self, row, column)
        await self.save(insert=True)
        cache.add_menu_item(self)
        menu.set_item(self, row, column)
        await menu.save()
        return self

    def build_component(self) -> quarrel.Component:
        if self.type is enums.MenuItemType.BUTTON:
            return components.MenuInterfaceButton(self)
        elif self.type is enums.MenuItemType.SELECT_MENU:
            return components.MenuInterfaceSelectMenu(self)
        raise RuntimeError("Unsupported menu item type")

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return embeds.menu_item(interaction, self)

    async def edit(
        self,
        style: Missing[enums.MenuItemStyle],
        label: Missing[str],
        disabled: Missing[bool],
        url: Missing[str],
        emoji: Missing[int],
        action: Missing[enums.MenuItemAction],
        action_options: Missing[list[int]],
    ) -> None:
        if style is not quarrel.MISSING:
            self.style = style
        if label is not quarrel.MISSING:
            self.label = label
        if disabled is not quarrel.MISSING:
            self.disabled = disabled
        if url is not quarrel.MISSING:
            self.url = url
        if emoji is not quarrel.MISSING:
            self.emoji = emoji
        if action is not quarrel.MISSING:
            self.action = action
        if action_options is not quarrel.MISSING:
            self.action_options = action_options
        await self.save()
        menu = self.menu
        if menu is not None:
            await menu.update_interfaces()

    @property
    def quarrel_style(self) -> quarrel.ButtonStyle:
        if self.style is enums.MenuItemStyle.BLURPLE:
            return quarrel.ButtonStyle.BLURPLE
        elif self.style is enums.MenuItemStyle.GRAY:
            return quarrel.ButtonStyle.GRAY
        elif self.style is enums.MenuItemStyle.GREEN:
            return quarrel.ButtonStyle.GREEN
        elif self.style is enums.MenuItemStyle.RED:
            return quarrel.ButtonStyle.RED
        else:
            return quarrel.ButtonStyle.GRAY
