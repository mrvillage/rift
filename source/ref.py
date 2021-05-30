import datetime
from bs4 import BeautifulSoup
from discord import Intents, AllowedMentions, Game
from discord.ext.commands import Bot, when_mentioned_or
import aiohttp
from .env import EMAIL, PASSWORD, __version__
from .errors import LoginError
from .data.db import execute_read_query
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
            timeout=aiohttp.ClientTimeout(total=30.0))
        self.staff = None
        self.auth_token = None

    async def update_pnw_session(self):
        login_data = {
            "email": EMAIL,
            "password": PASSWORD,
            "loginform": "Login"
        }
        try:
            async with self.pnw_session.request("POST", "https://politicsandwar.com/login/", data=login_data) as response:  # pylint: disable=line-too-long
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
        self.auth_token = data.find('input', {"name": "token"}).attrs['value']


intents = Intents.all()
bot = Rift(command_prefix=when_mentioned_or("?"),
           intents=intents,
           case_insensitive=True,
           allowed_mentions=AllowedMentions(replied_user=False),
           activity=Game(name=__version__),
           strip_after_prefix=True,
           help_command=EmbedHelpCommand())
