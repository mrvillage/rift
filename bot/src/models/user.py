from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import cache, models, utils
from ..bot import bot

__all__ = ("User",)

if TYPE_CHECKING:
    import uuid
    from typing import ClassVar, Optional

    import quarrel
    from typing_extensions import Self

    from ..types.models.user import User as UserData
    from ..types.quarrel import MemberOrUser


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class User:
    TABLE: ClassVar[str] = "users"
    PRIMARY_KEY: ClassVar[tuple[str]] = ("user_id",)
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    user_id: int
    nation_id: Optional[int]
    uuid: Optional[uuid.UUID]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: UserData) -> User:
        ...

    def to_dict(self) -> UserData:
        ...

    def update(self, data: User) -> User:
        ...

    @property
    def key(self) -> int:
        return self.user_id

    @property
    def nation(self) -> Optional[models.Nation]:
        return cache.get_nation(self.nation_id) if self.nation_id else None

    @property
    def user(self) -> Optional[quarrel.User]:
        return bot.get_user(self.user_id)

    @classmethod
    async def link(cls, user: MemberOrUser, nation: models.Nation) -> Self:
        self = cls(user_id=user.id, nation_id=nation.id, uuid=None)
        cache.add_user(self)
        await self.save(insert=True)
        return self
