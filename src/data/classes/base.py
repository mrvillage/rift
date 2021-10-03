from __future__ import annotations

__all__ = ("Makeable",)


class Makeable:
    async def make_attrs(self, *attrs: str) -> None:
        for attr in attrs:
            try:
                await getattr(self, f"_make_{attr}")()
            except Exception:
                pass
