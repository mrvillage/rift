from __future__ import annotations

from .. import models
from .base import RiftError

__all__ = ("NationNotInAllianceError",)


class NationNotInAllianceError(RiftError):
    def __init__(self, nation: models.Nation) -> None:
        self.nation: models.Nation = nation
