from __future__ import annotations

__all__ = ("GuildOnlyError", "MissingDiscordPermissionsError")

from .base import RiftError


class GuildOnlyError(RiftError):
    ...


class MissingDiscordPermissionsError(RiftError):
    ...
