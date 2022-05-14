from __future__ import annotations

from src import models

__all__ = ("DATA",)

DATA: dict[int, models.User] = {
    3001: models.User(user_id=3001, nation_id=1001, uuid=None)
}
for i in DATA.values():
    if i.nation_id is not None:
        DATA[i.nation_id] = i
