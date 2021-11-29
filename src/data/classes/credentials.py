from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import aiohttp

from ...cache import cache
from ...flags import CredentialsPermissions
from ...funcs import credentials
from .nation import Nation

__all__ = ("Credentials",)

if TYPE_CHECKING:
    from typing import Optional

    from _typings import CredentialsData


class Credentials:
    __slots__ = ("nation_id", "permissions", "_username", "_password", "_api_key")

    def __init__(self, data: CredentialsData) -> None:
        self.nation_id: int = data["nation"]
        self.permissions: CredentialsPermissions = CredentialsPermissions(
            data["permissions"]
        )
        self._username: str = data["username"]
        self._password: str = data["password"]
        self._api_key: str = data["api_key"]

    @property
    def username(self) -> Optional[str]:
        if self._username is None:
            return
        return credentials.decrypt_credential(bytes.fromhex(self._username))

    @property
    def password(self) -> Optional[str]:
        if self._password is None:
            return
        return credentials.decrypt_credential(bytes.fromhex(self._password))

    @property
    def api_key(self) -> Optional[str]:
        if self._api_key is None:
            return
        return credentials.decrypt_credential(bytes.fromhex(self._api_key))

    @property
    def nation(self) -> Optional[Nation]:
        return cache.get_nation(self.nation_id)

    def has_permission(self, permission: str) -> bool:
        return getattr(self.permissions, permission, False)

    def update(self, data: CredentialsData) -> None:
        self.permissions.flags = data["permissions"]
        self._username: str = data["username"]
        self._password: str = data["password"]
        self._api_key: str = data["api_key"]

    async def login(self, session: aiohttp.ClientSession) -> bool:
        async with session.request(
            "POST",
            "https://politicsandwar.com/login/",
            data={
                "email": self.username,
                "password": self.password,
                "loginform": "Login",
            },
        ) as response:
            return "login failure" not in (await response.text()).lower()
