from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import aiohttp
import discord
from discord.ext import commands

from .env import (
    APPLICATION_ID,
    DEBUG_APPLICATION_ID,
    PNW_EMAIL,
    PNW_PASSWORD,
    __version__,
)
from .help import EmbedHelpCommand

if TYPE_CHECKING:
    from .cache import Cache


class Rift(commands.Bot):
    bytes_avatar: bytes
    debug: bool

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)  # type: ignore
        print("Starting up!")
        self.pnw_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30.0)
        )
        self.auth_token: Optional[str] = None
        self.enable_debug: bool = False

    async def update_pnw_session(self):
        from .errors import LoginError

        login_data = {
            "email": PNW_EMAIL,
            "password": PNW_PASSWORD,
            "loginform": "Login",
        }
        try:
            async with self.pnw_session.request(
                "POST", "https://politicsandwar.com/login/", data=login_data
            ) as response:  # pylint: disable=line-too-long
                if "login failure" in (await response.text()).lower():
                    raise LoginError
        except LoginError:
            pass

    async def get_staff(self):
        ...

    async def close(self):
        from .data.db.connect import connection, notify_connection

        await connection.close()
        await notify_connection.close()  # type: ignore
        await self.pnw_session.close()
        await super().close()

    async def get_global_application_commands(self):
        if TYPE_CHECKING:
            assert isinstance(self.application_id, int)
        self.global_application_commands = await bot.http.get_global_commands(
            self.application_id
        )

    @property
    def cache(self) -> Cache:
        from .cache import cache

        return cache


intents = discord.Intents(
    dm_messages=True,
    guild_messages=True,
    guilds=True,
    members=True,
)
debug = False

ID = DEBUG_APPLICATION_ID if debug else APPLICATION_ID
bot = Rift(
    command_prefix=commands.when_mentioned_or("?"),
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(replied_user=False),
    activity=discord.Game(name=f"/help on {__version__}"),
    strip_after_prefix=True,
    help_command=EmbedHelpCommand(
        command_attrs={
            "type": (commands.CommandType.default, commands.CommandType.chat_input)
        }
    ),
    application_id=ID,
    debug_command_prefix="!!",
    debug_guild_id=654109011473596417,
    debug=debug,
    chunk_guilds_at_startup=True,
)


class RiftContext(commands.Context[Rift]):
    command: Optional[commands.Command[commands.Cog, Any, Any]]
