from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RiftError

if TYPE_CHECKING:

    import quarrel


class Response(RiftError):
    ...


class EmbedErrorResponse(Response):
    def __init__(self, embed: quarrel.Embed) -> None:
        self.embed: quarrel.Embed = embed

    def build_embed(self, interaction: quarrel.Interaction) -> quarrel.Embed:
        return self.embed
