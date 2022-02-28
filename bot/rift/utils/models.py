from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Protocol, Type, TypeVar

from .. import db

__all__ = ("model",)

if TYPE_CHECKING:
    from typing import Any

T = TypeVar("T", bound="Type[ModelProtocol]")


class ModelProtocol(Protocol):
    __slots__ = ("id",)
    TABLE: ClassVar[str]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: Any) -> ModelProtocol:
        ...


def model(class_: T) -> T:
    g: dict[str, Any] = {"db": db}
    exec(
        f"""
async def save(self) -> None:
    if self.id:
        await db.query("UPDATE {class_.TABLE} SET {", ".join(f"{name} = ${i+1}" for i, name in enumerate(class_.__slots__))} WHERE id = ${class_.__slots__.index("id")+1};",
        {", ".join(f"self.{name}" for name in class_.__slots__)},
        )
    else:
        id = await db.query("INSERT INTO {class_.TABLE} ({", ".join(i for i in class_.__slots__ if i != "id")}) VALUES ({", ".join(f"${i}" for i in range(1, len(class_.__slots__)))}) RETURNING id;", {", ".join(f"self.{name}" for name in class_.__slots__ if name != "id")})
        self.id = id[0]["id"]
    """,
        g,
    )
    exec(
        f"""
@classmethod
def from_dict(cls, data) -> None:
    return cls({", ".join(f'{name}=data["{name}"]' for name in class_.__slots__)})
    """,
        g,
    )
    class_.save = g["save"]
    class_.from_dict = g["from_dict"]
    return class_
