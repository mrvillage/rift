from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = (
    "FOOTER_TEXT",
    "PROVIDER_NAME",
)

if TYPE_CHECKING:
    from typing import Final

FOOTER_TEXT: Final[str] = "rift.mrvillage.dev"
PROVIDER_NAME: Final[str] = "Rift"
