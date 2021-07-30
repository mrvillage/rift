import datetime

import aiohttp
from bs4 import BeautifulSoup
from discord import AllowedMentions, Game, Intents
from discord.ext.commands import Bot, when_mentioned_or

from .data.db import execute_read_query
from .env import EMAIL, PASSWORD, __version__
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

    async def update_pnw_session(self):
        login_data = {"email": EMAIL, "password": PASSWORD, "loginform": "Login"}
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

    async def get_guild_prefix(self, guild_id):
        prefixes = [
            i
            for i in await execute_read_query(
                "SELECT prefix FROM prefixes WHERE guild_id = $1;", guild_id
            )
        ]
        if prefixes:
            return prefixes
        return default_prefixes

    get_guild_prefixes = get_guild_prefix

    async def get_slash_commands(self):
        from .env import TOKEN

        async with aiohttp.request(
            "GET",
            f"https://discord.com/api/v9/applications/{self.application_id}/commands",
            headers={"Authorization": f"Bot {TOKEN}"},
        ) as response:
            self.slash_commands = await response.json()


default_prefixes = ["?"]


async def get_prefix(rift: Rift, message):
    prefixes = await rift.get_guild_prefixes(message.guild.id)
    return when_mentioned_or(*prefixes)(rift, message)


bot = Rift(
    command_prefix=get_prefix,
    intents=Intents.all(),
    case_insensitive=True,
    allowed_mentions=AllowedMentions(replied_user=False),
    activity=Game(name=__version__),
    strip_after_prefix=True,
    help_command=EmbedHelpCommand(),
)
