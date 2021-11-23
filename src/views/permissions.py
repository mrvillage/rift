from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, List

import discord

from .. import funcs
from ..flags import Flags

__all__ = ("PermissionsSelector", "PermissionsSelect")

if TYPE_CHECKING:
    from _typings import Permission


class PermissionsSelector(discord.ui.View):
    def __init__(
        self,
        owner_id: int,
        save: Callable[[Flags], Coroutine[Any, Any, None]],
        flags: Flags,
        permissions: List[Permission],
    ) -> None:
        super().__init__()
        self.owner_id: int = owner_id
        self.save: Callable[[Flags], Coroutine[Any, Any, None]] = save
        self.flags: Flags = flags
        self.permissions: List[Permission] = permissions
        for i in range(0, len(self.permissions), 25):
            self.add_item(PermissionsSelect(self.flags, self.permissions[i : i + 25]))  # type: ignore

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user is None:
            return False
        return interaction.user.id == self.owner_id

    @discord.ui.button(label="Save", row=4, style=discord.ButtonStyle.green)
    async def save_button(
        self,
        button: discord.ui.Button[PermissionsSelector],
        interaction: discord.Interaction,
    ) -> None:
        await self.save(self.flags)
        if TYPE_CHECKING:
            assert interaction.user is not None
        await interaction.response.defer()
        self.stop()


class PermissionsSelect(discord.ui.Select[PermissionsSelector]):
    def __init__(self, flags: Flags, permissions: List[Permission]) -> None:
        super().__init__(
            min_values=0,
            max_values=len(permissions),
            options=[
                discord.SelectOption(
                    label=p["name"], value=p["value"], description=p["description"]
                )
                for p in permissions
            ],
        )
        self.flags: Flags = flags
        self.permissions: List[Permission] = permissions

    async def callback(self, interaction: discord.Interaction) -> None:
        if TYPE_CHECKING:
            assert interaction.user is not None
        enabled: List[str] = []
        disabled: List[str] = []
        for permission in self.permissions:
            if permission["value"] in self.values:
                if not getattr(self.flags, permission["value"]):
                    setattr(self.flags, permission["value"], True)
                    enabled.append(permission["name"])
            elif getattr(self.flags, permission["value"]):
                disabled.append(permission["name"])
                setattr(self.flags, permission["value"], False)
        await interaction.response.send_message(
            embed=funcs.get_embed_author_member(
                interaction.user,
                f"Enabled: {', '.join(f'`{name}`' for name in enabled) or 'None'}\nDisabled: {', '.join(f'`{name}`' for name in disabled) or 'None'}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )
