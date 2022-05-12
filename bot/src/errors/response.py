from __future__ import annotations

import quarrel

from .base import RiftError


class Response(RiftError):
    ...


class EmbedErrorResponse(Response):
    def __init__(self, embed: quarrel.Embed) -> None:
        self._embed: quarrel.Embed = embed

    @property
    def embed(self) -> quarrel.Embed:
        return self._embed
