from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("COMMAND_IS_GUILD_ONLY",)

if TYPE_CHECKING:
    from typing import Final

COMMAND_IS_GUILD_ONLY: Final[str] = "Sorry, this command can only be used in a server!"
