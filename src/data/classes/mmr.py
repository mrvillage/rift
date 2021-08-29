from ..query import query_mmr


class MMR:
    __slots__ = ("data",)

    def __init__(self, *, mmr_id=None):
        self.data = query_mmr(mmr_id=mmr_id)
