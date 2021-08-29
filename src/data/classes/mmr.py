from ..query import get_mmr


class MMR:
    __slots__ = ("data",)

    def __init__(self, *, mmr_id=None):
        self.data = get_mmr(mmr_id=mmr_id)
