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

    def to_dict(self) -> Any:
        ...


def model(class_: T) -> T:
    g: dict[str, Any] = {"db": db, "Any": Any}
    primary_key = getattr(class_, "PRIMARY_KEY", "id")
    if isinstance(primary_key, str):
        primary_key = (primary_key,)
    exec(
        f"""
async def save(self):
    if self.id:
        await db.query("UPDATE {class_.TABLE} SET {", ".join(f"{name} = ${i+1}" for i, name in enumerate(class_.__slots__))} WHERE {' AND '.join(f'{name} = ${class_.__slots__.index(name)+1}' for name in primary_key)});",
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
def from_dict(cls, data):
    return cls({", ".join(f'{name}=data["{name}"]' for name in class_.__slots__)})
    """,
        g,
    )
    exec(
        f"""
def to_dict(self):
    return {{{", ".join(f'"{name}": self.{name}' for name in class_.__slots__)}}}
    """,
        g,
    )
    class_.save = g["save"]
    class_.from_dict = g["from_dict"]
    class_.to_dict = g["to_dict"]
    return class_
