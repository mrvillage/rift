from ..query import get_mmr
from .base import Base


class MMR(Base):
    def __init__(self, *, mmr_id=None):
        self.data = get_mmr(mmr_id=mmr_id)
