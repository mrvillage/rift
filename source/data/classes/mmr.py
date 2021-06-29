from .base import Base
from ..query import get_mmr


class MMR(Base):
    def __init__(self, *, mmr_id=None):
        self.data = get_mmr(mmr_id=mmr_id)
