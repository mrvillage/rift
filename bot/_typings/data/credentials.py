from __future__ import annotations

from typing import TypedDict

__all__ = ("CredentialsData",)


class CredentialsData(TypedDict):
    nation: int
    permissions: int
    username: str
    password: str
    api_key: str
