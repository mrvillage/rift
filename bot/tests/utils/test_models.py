from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
from src import utils

if TYPE_CHECKING:
    from typing import ClassVar


# expecting error since save and from_dict are not yet defined for testing
@utils.model  # type: ignore
@attrs.define
class Model:
    TABLE: ClassVar[str] = "test"

    id: int
    name: str


def test_model():
    assert hasattr(Model, "id")
    assert hasattr(Model, "name")
    assert hasattr(Model, "TABLE")
    assert hasattr(Model, "save")
    assert hasattr(Model, "from_dict")
