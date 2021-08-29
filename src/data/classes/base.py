from __future__ import annotations


class Makeable:
    async def make_attrs(self, *attrs: str) -> None:
        for attr in attrs:
            await getattr(self, f"_make_{attr}")()
