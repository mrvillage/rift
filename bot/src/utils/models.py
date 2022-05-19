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

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: Any) -> ModelProtocol:
        ...

    def to_dict(self) -> Any:
        ...

    def update(self, data: Any) -> ModelProtocol:
        ...


def model(class_: T) -> T:
    g: dict[str, Any] = {"db": db}
    primary_key = getattr(class_, "PRIMARY_KEY", ("id",))
    increment = getattr(class_, "INCREMENT", ("id",))
    enums = getattr(class_, "ENUMS", ())
    flags = getattr(class_, "FLAGS", ())
    no_update = getattr(class_, "NO_UPDATE", ())
    ignore = getattr(class_, "IGNORE", ())
    slots = [i for i in class_.__slots__ if i not in ignore]
    if isinstance(primary_key, str):
        primary_key = (primary_key,)
    exec(
        f"""
async def save(self, insert = False):
    if {" and ".join(f"self.{i}" for i in primary_key)} and not insert:
        await db.query('UPDATE {class_.TABLE} SET {", ".join(f'"{name}" = ${i+1}' for i, name in enumerate(slots))} WHERE {" AND ".join(f'"{name}" = ${slots.index(name)+1}' for name in primary_key)};',
        {", ".join(f"self.{name}" if name not in enums and name not in flags else f"self.{name}.value" for name in slots)})
    else:
        id = await db.query('INSERT INTO {class_.TABLE} ({", ".join(f'"{i}"' for i in slots if i not in increment)}) VALUES ({", ".join(f"${index + 1}" for index in range(len([j for j in slots if j not in increment])))}){" RETURNING (" + ", ".join(f'"{i}"' for i in increment) + ");" if increment else ";"}', {", ".join(f"self.{name}" if name not in enums and name not in flags else f"self.{name}.value" for name in slots if name not in increment)})
        {'self.id = id[0]["id"]' if increment else ''}
    """,
        g,
    )
    exec(  # nosec
        f"""
async def delete(self):
    await db.query("DELETE FROM {class_.TABLE} WHERE {' AND '.join(f'{name} = ${index + 1}' for index, name in enumerate(primary_key))};", {", ".join(f"self.{name}" for name in primary_key)})
    """,
        g,
    )
    exec(
        f"""
@classmethod
def from_dict(cls, data):
    return cls({", ".join(f'{name}=data["{name}"]' for name in slots)})
    """,
        g,
    )
    exec(
        f"""
def to_dict(self):
    return {{{", ".join(f'"{name}": self.{name}' for name in slots)}}}
    """,
        g,
    )
    newline_with_spaces = "\n    "
    exec(
        f"""
def update(self, data):
    {newline_with_spaces.join(f'self.{name} = data.{name}' for name in slots if name not in no_update)}
    return self
    """,
        g,
    )
    class_.save = g["save"]
    class_.delete = g["delete"]
    class_.from_dict = g["from_dict"]
    class_.to_dict = g["to_dict"]
    class_.update = g["update"]
    return class_
