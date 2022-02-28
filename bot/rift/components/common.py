from __future__ import annotations

from typing import TYPE_CHECKING

import quarrel

__all__ = ("CommonButton", "CommonSelectMenu", "CommonGrid")

if TYPE_CHECKING:
    ...


class CommonButton(quarrel.Button):
    ...


class CommonSelectMenu(quarrel.SelectMenu):
    ...


class CommonGrid(quarrel.Grid):
    ...
