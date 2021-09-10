import datetime

import aiohttp
from bs4 import BeautifulSoup
from discord import AllowedMentions, Game, Intents
from discord.ext.commands import Bot, when_mentioned_or

from .data.db import execute_read_query
from .env import (
    APPLICATION_ID,
    DEBUG_APPLICATION_ID,
    PNW_EMAIL,
    PNW_PASSWORD,
    __version__,
)
from .errors import LoginError
from .help import EmbedHelpCommand


class Rift(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alliances_update = datetime.datetime.utcnow()
        self.nations_update = datetime.datetime.utcnow()
        self.cities_update = datetime.datetime.utcnow()
        self.prices_update = datetime.datetime.utcnow()
        print("Starting up!")
        self.pnw_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30.0)
        )
        self.staff = None
        self.auth_token = None
        self.cogs_loaded = False
        self.persistent_views_loaded = False
        self.subscribable_events = {
            "war_declaration",
        }

    async def update_pnw_session(self):
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
        self.staff = [i[0] for i in await execute_read_query("SELECT * FROM staff;")]
        return self.staff

    async def close(self):
        await self.pnw_session.close()
        await super().close()

    async def parse_token(self, content):
        data = BeautifulSoup(content, "html.parser")
        self.auth_token = data.find("input", {"name": "token"}).attrs["value"]  # type: ignore

    async def get_global_application_commands(self):
        self.application_id: int
        self.global_application_commands = await bot.http.get_global_commands(
            self.application_id
        )


intents = Intents(
    dm_messages=True, guild_messages=True, guilds=True, members=True, reactions=True
)
debug = False

ID = DEBUG_APPLICATION_ID if debug else APPLICATION_ID
bot = Rift(
    command_prefix=when_mentioned_or("?"),
    intents=intents,
    case_insensitive=True,
    allowed_mentions=AllowedMentions(replied_user=False),
    activity=Game(name=__version__),
    strip_after_prefix=True,
    help_command=EmbedHelpCommand(),
    application_id=ID,
    debug_command_prefix="!!",
    debug_guild_id=654109011473596417,
    debug=debug,
    chunk_guilds_at_startup=True,
)
